# Take password as input and evalute based on given criteria
function Test-PasswordStrength {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$Password
    )

    $Criteria = @{
        Length = 8
        Uppercase = 1
        Lowercase = 1
        Numeric = 1
        SpecialChar = 1
    }

    $Score = 0

    if ($Password.Length -ge $Criteria.Length) {
        $Score++
    }

    if ($Password -cmatch "[A-Z]") {
        $Score++
    }

    if ($Password -cmatch "[a-z]") {
        $Score++
    }

    if ($Password -cmatch "[0-9]") {
        $Score++
    }

    if ($Password -cmatch "[!@#\$%^&*\(\)_\+\-\=\[\]\{\};:'""<>,\.\?/\\|]") {
        $Score++
    }

    $Strength = switch ($Score) {
        0 { "Very Weak" }
        1 { "Weak" }
        2 { "Moderate" }
        3 { "Strong" }
        4 { "Very Strong" }
        default { "Unknown" }
    }

    [PSCustomObject]@{
        Password = $Password
        Score = $Score
        Strength = $Strength
    }
}

# Usage example:
$enteredPassword = Read-Host -AsSecureString "Enter a password"
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($enteredPassword))
$strengthResult = Test-PasswordStrength -Password $plainPassword
Write-Output $strengthResult
