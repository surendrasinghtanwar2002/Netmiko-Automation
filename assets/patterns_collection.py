                                        ## basic user prompts ##
basic_user_prompt = {
    r'Proceed with reload? [confirm]': 'yes',
    r'Erasing the nvram filesystem will remove all configuration files!\nContinue? [confirm]': 'yes',
    r'Shutdown interface? [yes/no]:': 'yes',
    r'Destination filename [startup-config]?': 'yes',
    r'Delete filename? [confirm]': 'yes',
    r'Apply configuration changes? [yes/no]:':'yes',
    r'Are you sure you want to reload? [confirm]': 'yes',
    r'Would you like to save your configuration? [yes/no]:': 'yes',
    r'Apply changes to all interfaces in the range? [yes/no]:': 'yes',
    r'Delete all files? [yes/no]:': 'yes'
}
                                        ## error prompt handling ##
error_prompt_handling = {
    "success": r'^(.*success|completed|done|executed).*|.*(success|ok|valid).*|.*finished.*)$',
    "command_error": r'(?i)^(%.*\bcommand)',
    "invalid_error": r'(?i)^.*% Incomplete command\.$',
    "authentication_error": r'(?i)\b(authentication (failed|required)|login error|invalid credentials|access denied|user not authorized|password expired|account locked|failed to authenticate|authentication timeout)\b',
    "common_error": r'(?i)(configuration.*mode|incomplete command|invalid input detected|permission denied|duplicate.*entry)'
    
}