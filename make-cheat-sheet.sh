function echo_run {
    echo "\$ $1"

    # LIES!
    # This allows me to use this code for testing with
    #   python 2 and python3
    # whilst also producing documentation
    #   combining documentation with testing has a lot of
    #   benefits

    command=$(echo $1 | sed "s_clixpath_$python -m clixpath_")
    eval "$command"
}



echo_run "echo '{\"one\": 1}' | genson  | short_schema"
echo_run "echo '[{\"one\": 1, \"two\": [1]}, {\"one\": 2}]' | genson  | short_schema"
