#!/usr/bin/env bash

ll='ls -la --color'

FG_RED=31

BG_RED=41
BG_GREEN=42
BG_YELLOW=43
BG_BLUE=44
BG_MAGENTA=45
BG_CYAN=46

# Source project configuration
SOURCE_PROJECT_DIR='../hvss-calculator-lab'

if [ ! -z "$1" ]; then
    SOURCE_PROJECT_DIR="$1"
else
    echo -e "\nNo Source project directory specified, using default:\t$SOURCE_PROJECT_DIR\n"
fi

SOURCE_PROJECT_MODELS_DIR="$SOURCE_PROJECT_DIR/models"
SOURCE_PROJECT_TRAINING_DATA_FILE="$SOURCE_PROJECT_DIR/TrainingData.xlsx"

TARGET_PROJECT_DIR="$(pwd)"
TARGET_PROJECT_MODELS_DIR="$TARGET_PROJECT_DIR/hvss_calc/Models"
TARGET_PROJECT_TRAINING_DATA_FILE="$TARGET_PROJECT_DIR/hvss_calc/tests/TrainingData.xlsx"

set_color(){
    COLOR="$1"
    echo -e "\e[${COLOR}m\n "
}

reset_color(){
    echo -e "\e[0m"
}

show_section_header(){
    COLOR="$1"
    MESSAGE="$2"
    echo -e "\e[${COLOR}m\n\n-----  $MESSAGE  -----\n\e[0m"
}

show_section_footer(){
    COLOR="$1"
    echo -e "\e[${COLOR}m\n \e[0m"
}

show_project_config(){
    LOCATION="$1"
    COLOR="$2"
    MESSAGE="$LOCATION project configuration"
    show_section_header "$COLOR" "$MESSAGE"

    eval LOCATION_PROJECT_DIR="\$${LOCATION}_PROJECT_DIR"
    eval LOCATION_PROJECT_MODELS_DIR="\$${LOCATION}_PROJECT_MODELS_DIR"
    eval LOCATION_PROJECT_TRAINING_DATA_FILE="\$${LOCATION}_PROJECT_TRAINING_DATA_FILE"

    echo -e "$LOCATION project directory:\t\t$LOCATION_PROJECT_DIR"
    echo -e "$LOCATION project Models directory:\t$LOCATION_PROJECT_MODELS_DIR"
    echo -e "$LOCATION project Training Data file:\t$LOCATION_PROJECT_TRAINING_DATA_FILE"
    echo
    echo -e "\n$LOCATION project directory:\t\t$LOCATION_PROJECT_DIR"
    $ll "$LOCATION_PROJECT_DIR"
    echo -e "\n$LOCATION project Models directory:\t$LOCATION_PROJECT_MODELS_DIR"
    $ll "$LOCATION_PROJECT_MODELS_DIR"
    echo -e "\n$LOCATION project Training Data file:\t$LOCATION_PROJECT_TRAINING_DATA_FILE"
    $ll "$LOCATION_PROJECT_TRAINING_DATA_FILE"
    echo
}

show_last_commits() {
    COLOR="$1"
    MESSAGE="$2"
    echo -e "\e[${COLOR}m\n\n-----  $MESSAGE  -----\n\e[0m"
    git log -n 2
    echo -e "\e[${COLOR}m\n \e[0m"

}

git_update() {
    if [ -z "$1" ]; then
        echo "ERROR: No project directory specified."
        return 1
    fi

    cd "$1" || exit
    echo -e "\nUpdating git repository in $(pwd)"

    git branch
    if [ -n "$(git status --porcelain)" ]; then
        set_color "$BG_RED"
        # echo git stash push -m "-----  Automatically stashed by ML model update script  -----"
        git stash push -m "-----  Automatically stashed by ML model update script  -----"
        reset_color
    fi
    git checkout main || exit
    git branch
    git status
    show_last_commits "$BG_BLUE" "Two last commits before update"

    echo -e "\e[7m\n "
    # echo -e "git pull ... $(pwd)"
    git pull
    echo -e " \n \e[0m"

    show_last_commits "$BG_GREEN" "Two last commits after update"
}

git_create_branch() {
    BRANCH_NAME="$1"
    echo -e "\nCreating new branch... $BRANCH_NAME"
    git checkout -b "$BRANCH_NAME"
}

copy_models(){
    echo -e "\nCopying ML model and training data files... $BRANCH_NAME"
    cp -vr "$SOURCE_PROJECT_MODELS_DIR"/* "$TARGET_PROJECT_MODELS_DIR"
    cp -v  "$SOURCE_PROJECT_TRAINING_DATA_FILE" "$TARGET_PROJECT_TRAINING_DATA_FILE"
    echo
}

update_ui_model_version() {
    echo -e "Updating UI ML build date and ID ..."
    echo -e "New ml_models_build_date: $ml_models_build_date"
    echo -e "New ml_models_build_id:   $ml_models_build_id\n"
    # Override version file with heredoc using cat
    version_file_name='./static/fancy/resources/version.js'
    echo -e "Overriding version file $version_file_name ..."
    ls -la $version_file_name
    echo -e "\nOld content:"
    cat $version_file_name
    cat > $version_file_name <<EOF
const ml_models_build_date = '$ml_models_build_date';
const ml_models_build_id = '$ml_models_build_id';
EOF
    echo -e "\nNew content:"
    cat $version_file_name
    echo
}

get_ml_models_build_date_and_id() {
    # Get ML models last commit ID
    ml_models_commit_id=$(git rev-parse --verify HEAD)
    ml_models_build_id=${ml_models_commit_id:0:5}
    # Get ML models last commit date
    ml_models_build_date=$(git show -s --format=%cd --date=format:'%Y-%m-%d-%H%M%S%z' "$ml_models_commit_id")
    echo -e "\nML models build date:\t$ml_models_build_date"
    echo -e "ML models build id:\t$ml_models_build_id\n"
}

test() {
    echo "Running Test function..."
    # copy_models
    get_ml_models_build_date_and_id
    update_ui_model_version
}

main() {
    # Save current branch
    echo -e "\nCurrent directory: $(pwd)"
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "Current branch is $current_branch"

    echo -e "\nSwitching to Source project...\n"
    show_project_config "SOURCE" "$BG_CYAN"
    git_update "$SOURCE_PROJECT_DIR"
    # Get ML models build date and ID
    get_ml_models_build_date_and_id
    echo -e "\nMain ml_models_build_date:\t$ml_models_build_date"
    echo -e "Main ml_models_build_id:\t$ml_models_build_id\n"

    echo -e "\nSwitching to Target project...\n"
    show_project_config "TARGET" "$BG_YELLOW"
    git_update "$TARGET_PROJECT_DIR"

    new_models_branch="feature/ml-model/build_${ml_models_build_id}_$ml_models_build_date"
    git_create_branch "$new_models_branch"
    copy_models
    update_ui_model_version

    git add .
    git status
    git commit -m "Updated ML models and training data file. ML models build ID: $ml_models_build_id."
    echo
    git status
    echo -e "\nPushing updated models' branch ($new_models_branch) and setting the remote as upstream..."
    git push --set-upstream origin "$new_models_branch"

    # TODO: Build new docker image and push it.
    # run_docker_build_and_publish.sh

    echo -e "\nSwitching back to original branch...\n"
    git checkout "$current_branch"
    echo "Back on $current_branch"
    echo -e "\nRetriving stashed changes back...\n"
    git stash pop

    echo -e "\n----- ML model update complited ------\n"
}

# Run test function
# test

# Running main function
main
