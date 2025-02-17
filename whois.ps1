$pythonProgramPath = cmd /c "where python" '2>&1'
$pythonScriptPath = "whoisip.py" 
$arg = "8.8.8.8"
$pythonOutput = & $pythonProgramPath $pythonScriptPath $arg
$pythonOutput