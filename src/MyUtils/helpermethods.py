from datetime import datetime
import time
# flake8: noqa: E302, W501
class MyHelpers:  
    def get_file_contents(file_path):
        """

        Reads the contents of a file.

        Args:
            file_path: The path to the file.

        Returns:
            The contents of the file as a string.
        """
        with open(file_path, 'r') as file:
            return file.read()

    def read_file_with_retry(file_paths, max_retries=3, retry_delay=1):
        """
        Attempts to read a file from a list of paths, retrying if FileNotFoundError occurs.

        Args:
            file_paths: A list of file paths to attempt.
            max_retries: The maximum number of retry attempts.
            retry_delay: The delay in seconds between retries.

        Returns:
            The content of the file as a string, or None if all attempts fail.
        """
        for attempt in range(max_retries):
            for file_path in file_paths:
                try:
                    with open(file_path, 'r') as file:
                        return file.read()
                except FileNotFoundError:
                    print(f"File not found: {file_path}. Attempt {attempt + 1} of {max_retries}.")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        print("Max retries exceeded. Could not find any of the specified files.")
        return None
    
    def get_dt_now():
        """
        Returns the current date and time as a string.

        Returns:
            The current date and time as a string.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def clear_file_rplus(filename):
        try:
            with open(filename, "r+") as file:
                if file.truncate(0) is None:
                    file.close()
                    return True
        except (IOError, OSError):
            if IOError.errno == 2:
                print(f"IO Err: {IOError} - Could not clear {filename}")
            if OSError.errno == 13:
                print(f"OS Err: {OSError} - Could not clear {filename}")
            return False
        
    def print_log_contents(log_type: str) -> None:
        """Helper method to print different types of log contents.
        
        Args:
            log_type: str - Type of logs to print ('none', 'all', 'errors', 'events')
        """
        if log_type.lower() == "none":
            print("No logs will be printed to the console!")
            return
            
    def print_error_logs(content: str) -> None:
        """Print error logs and count from content."""
        error_count = 0
        print("[Last Game's Error Logs:]")
        for line in content.split('\n'):
            if "[ERROR]" in line or "[CRITICAL]" in line:
                error_count += 1
                print(line)
        print(f"Error Count: {error_count}")
        if error_count == 0:
            print("No errors were found in the logs.")
        print()

    def print_event_logs(content: str) -> None:
        """Print event logs from content."""
        print("[Last Game's Events:]")
        print(content)