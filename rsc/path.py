import os

# Get the path to the file in folder2
file_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'contextual_menu.ui')

# Ensure the path resolves correctly
file_path = os.path.abspath(file_path)
print(file_path)  # Debugging: print the resolved path
