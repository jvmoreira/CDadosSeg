### Análise de APKs

Este programa recebe como parâmetro um diretório contendo arquivos `.xml`, representando o `AndroidManifest` de determinado aplicativo, e exibe a lista de permissões **do sistema Android** que são utilizadas.
Isso significa que, caso um aplicativo utilize uma permissão externa ao sistema Android, esta permissão não será considerada. Ex: `com.app.permission.PERMISSION_NAME`.

#### Execução
`python TP2p1.py manifests`
