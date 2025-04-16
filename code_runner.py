def run_code(code_str):
    """Run Python code and return its output"""
    try:
        # Create a string buffer to capture the output
        output = []
        
        # Define a custom print function
        def custom_print(*args, **kwargs):
            output.append(' '.join(str(arg) for arg in args))
        
        # Create a local namespace with our custom print function
        local_dict = {'print': custom_print}
        
        # Execute the code and capture the return value
        result = exec(code_str, {}, local_dict)
        
        # If there's no print output but the code executed successfully
        if not output and result is None:
            return "Code executed successfully with no output."
        
        # Return the captured output
        return '\n'.join(output)
    except Exception as e:
        return f"Error: {str(e)}" 