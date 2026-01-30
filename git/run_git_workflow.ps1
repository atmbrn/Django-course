<#
PowerShell script to perform the Git exercise described in homework.md.
Run this script from the repository root (where `project.txt` is located).
This script is interactive and will pause before destructive actions.
#>

param(
    [switch]$DoHardReset
)

function Confirm-Continue($msg){
    $r = Read-Host "$msg (y/n)"
    return $r -eq 'y' -or $r -eq 'Y'
}

# Ensure we're inside a git repo
if (-not (git rev-parse --is-inside-work-tree 2>$null)){
    Write-Host "This directory is not a git repository. Initialize one first or run this inside your repo." -ForegroundColor Red
    exit 1
}

# 1) Initial commit on main (if no commits yet)
if (-not (git rev-parse --verify HEAD 2>$null)){
    git checkout -b main
    git add project.txt
    git commit -m "Initial project structure"
    Write-Host "Created initial commit on 'main'."
} else {
    Write-Host "Repository already has commits. Skipping initial commit step."
}

# 2) feature-login branch and commits
git checkout -b feature-login
Add-Content -Path project.txt -Value "- Login system"
git add project.txt
git commit -m "Add login feature"

Add-Content -Path project.txt -Value "- Remember me option"
git add project.txt
git commit -m "Extend login feature"
Write-Host "feature-login: two commits created." -ForegroundColor Green

# 3) Merge into main
git checkout main
git merge --no-ff feature-login -m "Merge feature-login"
Write-Host "Merged 'feature-login' into 'main'." -ForegroundColor Green

# 4) feature-payment branch with an error
git checkout -b feature-payment
# change version
(Get-Content project.txt) -replace 'Version: 1.0','Version: 2.0' | Set-Content project.txt
# add payment feature
Add-Content -Path project.txt -Value "- Payment system"

git add project.txt
git commit -m "Add payment feature"

# Introduce the intentional 'error' by removing the Project line
(Get-Content project.txt) | Where-Object { $_ -ne 'Project: Git Practice' } | Set-Content project.txt

git add project.txt
git commit -m "Update payment logic"

Write-Host "feature-payment: made version change, added payment, then committed a removal (intentional error)." -ForegroundColor Yellow

# Show log to user
Write-Host "Recent commits (on current branch):" -ForegroundColor Cyan
git --no-pager log --oneline --decorate -n 10

# 5) Reset steps (soft -> mixed -> optional hard)
Write-Host "\nNow you'll perform resets. First, inspect the log and choose the commit hash BEFORE the erroneous commit." -ForegroundColor Cyan
git --no-pager log --oneline --decorate -n 20

$hash = Read-Host "Enter the commit hash to reset to (the commit BEFORE the error)"
if (-not $hash){ Write-Host "No hash provided, skipping reset steps."; }
else {
    Write-Host "Performing: git reset --soft $hash"
    git reset --soft $hash
    git status

    Write-Host "Now performing: git reset --mixed $hash"
    git reset --mixed $hash
    git status

    if ($DoHardReset -or (Confirm-Continue "Do you want to run 'git reset --hard $hash' (DANGEROUS)?")){
        Write-Host "Performing: git reset --hard $hash"
        git reset --hard $hash
        Write-Host "Hard reset performed. DO NOT push this state to remote if you want to preserve history." -ForegroundColor Red
    } else {
        Write-Host "Skipped hard reset." -ForegroundColor Green
    }
}

# 6) Show reflog and provide restore option
Write-Host "\nGit reflog (recent actions):" -ForegroundColor Cyan
git reflog -n 30
if (Confirm-Continue "Do you want to restore a state from reflog now?"){
    $refl = Read-Host "Enter the reflog reference (e.g. HEAD@{3}) or the full commit hash"
    if ($refl){
        Write-Host "Restoring with: git reset --hard $refl"
        if (Confirm-Continue "Are you sure to run the hard reset to restore (this will change working tree)?"){
            git reset --hard $refl
            Write-Host "Restored to $refl" -ForegroundColor Green
        } else { Write-Host "Restore cancelled." }
    }
}

# 7) Cleanup: delete feature-payment branch (local)
if (Confirm-Continue "Delete local branch 'feature-payment'? (y deletes if merged, n to skip)"){
    git branch -d feature-payment 2>$null
    if ($LASTEXITCODE -ne 0){
        Write-Host "Branch wasn't fully merged; deleting forcefully with -D." -ForegroundColor Yellow
        git branch -D feature-payment
    }
    Write-Host "feature-payment deleted locally." -ForegroundColor Green
}

Write-Host "\nScript finished. Review the repo state and push 'main' when ready: 'git push origin main'" -ForegroundColor Cyan

# End of script
