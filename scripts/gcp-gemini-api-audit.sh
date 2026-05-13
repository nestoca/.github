#!/bin/bash

set -euo pipefail

GEMINI_API="generativelanguage.googleapis.com"
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== GCP Gemini API & Unrestricted API Keys Audit ===${NC}\n"

check_gcloud() {
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}Error: gcloud CLI not found. Please install it first.${NC}"
        echo "Visit: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
}

get_all_projects() {
    echo -e "${BLUE}Fetching all accessible GCP projects...${NC}"
    gcloud projects list --format="value(projectId)" 2>/dev/null || {
        echo -e "${RED}Error: Failed to list projects. Please ensure you're authenticated.${NC}"
        echo "Run: gcloud auth login"
        exit 1
    }
}

check_api_enabled() {
    local project=$1
    gcloud services list --enabled --project="$project" --format="value(config.name)" 2>/dev/null | grep -q "^${GEMINI_API}$"
}

check_unrestricted_keys() {
    local project=$1
    local has_unrestricted=false
    
    local keys=$(gcloud alpha services api-keys list --project="$project" --format="json" 2>/dev/null || echo "[]")
    
    if [ "$keys" = "[]" ] || [ -z "$keys" ]; then
        return 1
    fi
    
    echo "$keys" | jq -r '.[] | select(.restrictions == null or .restrictions == {} or (.restrictions.apiTargets == null and .restrictions.browserKeyRestrictions == null and .restrictions.serverKeyRestrictions == null and .restrictions.androidKeyRestrictions == null and .restrictions.iosKeyRestrictions == null)) | .name' 2>/dev/null | grep -q . && has_unrestricted=true
    
    if [ "$has_unrestricted" = true ]; then
        return 0
    else
        return 1
    fi
}

main() {
    check_gcloud
    
    local projects=$(get_all_projects)
    
    if [ -z "$projects" ]; then
        echo -e "${YELLOW}No projects found or insufficient permissions.${NC}"
        exit 0
    fi
    
    local total_count=0
    local gemini_enabled_count=0
    local unrestricted_keys_count=0
    
    declare -a projects_with_gemini=()
    declare -a projects_with_unrestricted=()
    
    echo -e "\n${BLUE}Scanning projects for Gemini API (${GEMINI_API})...${NC}\n"
    
    while IFS= read -r project; do
        ((total_count++))
        echo -ne "Checking project: ${project}..."
        
        if check_api_enabled "$project"; then
            ((gemini_enabled_count++))
            projects_with_gemini+=("$project")
            echo -e " ${GREEN}[Gemini API ENABLED]${NC}"
            
            echo -ne "  └─ Checking for unrestricted API keys..."
            if check_unrestricted_keys "$project"; then
                ((unrestricted_keys_count++))
                projects_with_unrestricted+=("$project")
                echo -e " ${RED}[UNRESTRICTED KEYS FOUND]${NC}"
            else
                echo -e " ${GREEN}[OK - No unrestricted keys]${NC}"
            fi
        else
            echo -e " [Not enabled]"
        fi
    done <<< "$projects"
    
    echo -e "\n${BLUE}=== Summary ===${NC}"
    echo -e "Total projects scanned: ${total_count}"
    echo -e "Projects with Gemini API enabled: ${GREEN}${gemini_enabled_count}${NC}"
    echo -e "Projects with unrestricted API keys: ${RED}${unrestricted_keys_count}${NC}"
    
    if [ ${gemini_enabled_count} -gt 0 ]; then
        echo -e "\n${BLUE}=== Projects with Gemini API Enabled ===${NC}"
        printf '%s\n' "${projects_with_gemini[@]}"
    fi
    
    if [ ${unrestricted_keys_count} -gt 0 ]; then
        echo -e "\n${RED}=== ⚠️  PROJECTS REQUIRING ACTION (Unrestricted API Keys) ===${NC}"
        printf '%s\n' "${projects_with_unrestricted[@]}"
        
        echo -e "\n${YELLOW}To fix unrestricted API keys, run:${NC}"
        echo -e "gcloud alpha services api-keys list --project=PROJECT_ID"
        echo -e "gcloud alpha services api-keys update KEY_ID --project=PROJECT_ID --api-target=service=SERVICE_NAME"
        echo -e "\nOr visit: https://console.cloud.google.com/apis/credentials"
    fi
    
    if [ ${gemini_enabled_count} -eq 0 ]; then
        echo -e "\n${GREEN}✓ No projects found with Gemini API enabled.${NC}"
    fi
}

main "$@"
