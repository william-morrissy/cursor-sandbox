#!/bin/bash

# Cursor Demo Reset Script
# This script resets the demo environment to its baseline state

echo "🔄 Resetting Cursor demo environment to baseline..."

# Store the baseline files
BASELINE_DIR=".demo-baseline"

# Function to create baseline if it doesn't exist
create_baseline() {
    if [ ! -d "$BASELINE_DIR" ]; then
        echo "📦 Creating baseline backup..."
        mkdir -p "$BASELINE_DIR"
        
        # Copy all demo files to baseline
        cp -r backend "$BASELINE_DIR/" 2>/dev/null || true
        cp -r frontend "$BASELINE_DIR/" 2>/dev/null || true
        cp -r .cursor "$BASELINE_DIR/" 2>/dev/null || true
        cp README.md "$BASELINE_DIR/" 2>/dev/null || true
        cp .gitignore "$BASELINE_DIR/" 2>/dev/null || true
        
        echo "✅ Baseline created successfully!"
    fi
}

# Function to restore from baseline
restore_baseline() {
    if [ -d "$BASELINE_DIR" ]; then
        echo "♻️  Restoring files from baseline..."
        
        # Remove current demo files
        rm -rf backend frontend
        
        # Restore from baseline
        cp -r "$BASELINE_DIR/backend" . 2>/dev/null || true
        cp -r "$BASELINE_DIR/frontend" . 2>/dev/null || true
        cp -r "$BASELINE_DIR/.cursor" . 2>/dev/null || true
        cp "$BASELINE_DIR/README.md" . 2>/dev/null || true
        cp "$BASELINE_DIR/.gitignore" . 2>/dev/null || true
        
        echo "✅ Demo environment restored to baseline!"
    else
        echo "⚠️  No baseline found. Creating one now..."
        create_baseline
    fi
}

# Reset git if needed (but keep the baseline)
reset_git() {
    if [ -d ".git" ]; then
        echo "🔀 Resetting git state..."
        git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
        git reset --hard 2>/dev/null || true
        echo "✅ Git state reset!"
    fi
}

# Main execution
case "${1:-restore}" in
    "create")
        create_baseline
        ;;
    "restore"|*)
        restore_baseline
        reset_git
        ;;
esac

echo ""
echo "🎯 Demo environment is ready!"
echo "📖 Check DEMO_WALKTHROUGH.md for the demo script"
echo ""

