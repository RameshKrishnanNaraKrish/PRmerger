import subprocess
import sys

def validate_syntax(modified_files):
    has_errors = False
    files = modified_files.split(',')

    for file in files:
        try:
            if file.endswith('.js'):
                # Validate JavaScript files using eslint
                result = subprocess.run(['eslint', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.py'):
                # Validate Python files using pylint
                result = subprocess.run(['pylint', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.sh'):
                # Validate Shell scripts using shellcheck
                result = subprocess.run(['shellcheck', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.tf'):
                # Validate Terraform files using terraform validate
                result = subprocess.run(['terraform', 'validate', '-json'], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.groovy'):
                # Validate Groovy files using groovyc
                result = subprocess.run(['groovyc', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.yml') or file.endswith('.yaml'):
                # Validate YAML files using yamllint
                result = subprocess.run(['yamllint', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.json'):
                # Validate JSON files using jq
                result = subprocess.run(['jq', '.', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.java'):
                # Validate Java files using javac
                result = subprocess.run(['javac', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            elif file.endswith('.html'):
                # Validate HTML files using tidy
                result = subprocess.run(['tidy', '-qe', file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Syntax issues found in {file}")
                    has_errors = True

            else:
                # No validation rules for other file types
                print(f"No syntax validation rules defined for {file}")

        except Exception as e:
            print(f"Error validating {file}: {e}")
            has_errors = True

    if has_errors:
        raise Exception("Syntax validation failed. Please fix the issues and try again.")
    else:
        print("Syntax validation passed successfully.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_syntax.py <modified_files>")
        sys.exit(1)

    modified_files = sys.argv[1]
    validate_syntax(modified_files)

if __name__ == '__main__':
    main()
