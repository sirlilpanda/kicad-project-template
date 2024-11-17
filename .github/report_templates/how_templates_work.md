# how the templates work

templates work by using a json file to fill in the templating spots. for more information on the templates checkout [mustache templates](https://mustache.github.io/). these templates use a json file format as what they call a "hash" to fill out the templates. the hashs for each of these templates are layout at the top of each of the `.mustache` files in a comment. These are also the hashes outputted by the processing scripts. usages for these scripts are at the top of the file.

if any schema says bool this actually means the value is either something or either doesnt exist/null.