def call(String modifiedFiles) {
    def hasErrors = false
    def files = modifiedFiles.split(',')

    files.each { file ->
        if (file.endsWith('.js')) {
            // Validate JavaScript files using eslint
            def result = sh(
                script: "eslint ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.py')) {
            // Validate Python files using pylint
            def result = sh(
                script: "pylint ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.sh')) {
            // Validate Shell scripts using shellcheck
            def result = sh(
                script: "shellcheck ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.tf')) {
            // Validate Terraform files using terraform validate
            def result = sh(
                script: "terraform validate -json | jq .",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.groovy')) {
            // Validate Groovy files using groovyc
            def result = sh(
                script: "groovyc ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.yml') || file.endsWith('.yaml')) {
            // Validate YAML files using yamllint
            def result = sh(
                script: "yamllint ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.json')) {
            // Validate JSON files using jq
            def result = sh(
                script: "jq . ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.java')) {
            // Validate Java files using javac
            def result = sh(
                script: "javac ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        } else if (file.endsWith('.html')) {
            // Validate HTML files using tidy
            def result = sh(
                script: "tidy -qe ${file}",
                returnStatus: true
            )
            if (result != 0) {
                echo "Syntax issues found in ${file}"
                hasErrors = true
            }
        else {
            echo "No syntax validation rules defined for ${file}"
        }
    }

    if (hasErrors) {
        error "Syntax validation failed. Please fix the issues and try again."
    } else {
        echo "Syntax validation passed successfully."
    }
}
