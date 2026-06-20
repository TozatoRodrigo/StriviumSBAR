# Guia de Configuração de Deploy

Este guia descreve os passos necessários para configurar o ambiente do GitHub para o deploy automatizado da aplicação.

## 1. Regra de Proteção de Branch (Obrigatório)

Para garantir que o workflow de deploy (`deploy.yml`) só seja executado em código que já passou nos testes de CI (`ci.yml`), configure uma regra de proteção para o branch `main`.

1.  Vá para **Settings > Branches** no seu repositório GitHub.
2.  Clique em **Add branch protection rule**.
3.  Em **Branch name pattern**, digite `main`.
4.  Marque a opção **Require status checks to pass before merging**.
5.  Na caixa de busca que aparecer, procure e selecione o status check: `Lint, Test and Security Check`. Este é o nome do job no nosso arquivo `ci.yml`.
6.  Clique em **Create**.

Com essa regra, nenhum Pull Request poderá ser mesclado ao `main` sem que o CI passe, garantindo a integridade do código que será implantado.

## 2. Configuração de Ambientes no GitHub

Para que o deploy manual funcione, você precisa configurar os ambientes no seu repositório.

1.  Vá para **Settings > Environments** no seu repositório GitHub.
2.  Clique em **New environment**.
3.  Crie um ambiente chamado `production` (para GCP, Android e iOS) e outro chamado `production-magalu` (para a VM).
4.  Em **Environment protection rules** para cada ambiente, marque **Required reviewers**.
5.  Adicione as pessoas ou times que poderão aprovar os deploys.
6.  Clique em **Configure environment**.

## 3. Configuração de Secrets

As pipelines de deploy precisam de algumas chaves de acesso (secrets) para autenticar nos serviços das lojas de aplicativos e para assinar os builds.

Vá para **Settings > Secrets and variables > Actions** e adicione os seguintes secrets:

### 3.1 iOS (Apple App Store)

Para o deploy no iOS, o Fastlane utiliza algumas variáveis de ambiente para autenticação e assinatura.

-   `FASTLANE_USER`: Seu Apple ID (ex: `seuemail@exemplo.com`).
-   `FASTLANE_PASSWORD`: Uma senha específica de aplicativo gerada no site da Apple. [Como gerar](https://support.apple.com/pt-br/102654).
-   `MATCH_PASSWORD`: A senha que você usou para criptografar seu repositório de certificados do Fastlane Match.
-   `MATCH_GIT_PRIVATE_KEY`: A chave SSH privada para acessar o repositório de certificados do Fastlane Match.

**Nota sobre Fastlane Match:** É altamente recomendado usar o [Fastlane Match](https://docs.fastlane.tools/actions/match/) para gerenciar os certificados de assinatura e perfis de provisionamento do iOS. Você precisará configurar um repositório Git privado para armazenar esses arquivos.

### 3.2 Android (Google Play Store)

Para o deploy no Android, você precisará de uma chave de serviço do Google Cloud para autenticar com a API do Google Play.

-   `GOOGLE_PLAY_CREDENTIALS`: O conteúdo do arquivo JSON da sua chave de serviço do Google Cloud. [Como obter](https://docs.fastlane.tools/actions/supply/#setup).

### 3.3 Web (Google Cloud Platform)

Para o deploy da aplicação web estática no Google Cloud Storage.

-   `GCP_SA_KEY`: A chave da sua conta de serviço do Google Cloud em formato JSON. Essa conta de serviço precisa ter permissão de **Storage Object Admin** (`roles/storage.objectAdmin`) no bucket de destino. [Como criar e obter a chave](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).
-   `GCS_BUCKET`: O nome do bucket no Google Cloud Storage para onde os arquivos serão enviados. Ex: `gs://meu-site-estatico`.

### 3.4 Deploy Web na VM (Magalu Cloud)

Para o deploy da aplicação web via SCP para a sua máquina virtual.

-   `MAGALU_HOST`: O endereço de IP ou hostname da sua VM na Magalu Cloud.
-   `MAGALU_USERNAME`: O nome de usuário para a conexão SSH (ex: `ubuntu`, `ec2-user`).
-   `MAGALU_SSH_KEY`: A chave SSH privada, sem senha, para autenticar na sua VM.

### 3.5 Assinatura do App Android

Para assinar o build de release do Android, você precisará de um keystore.

1.  Gere um keystore:
    ```bash
    keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
    ```
2.  Converta o keystore para base64 para armazená-lo como um secret:
    ```bash
    base64 my-release-key.keystore > keystore.b64
    ```
3.  Adicione os seguintes secrets no GitHub:
    -   `ANDROID_KEYSTORE_BASE64`: O conteúdo do arquivo `keystore.b64`.
    -   `ANDROID_KEYSTORE_PASSWORD`: A senha que você definiu para o keystore.
    -   `ANDROID_KEY_ALIAS`: O alias que você definiu (`my-key-alias` no exemplo).
    -   `ANDROID_KEY_PASSWORD`: A senha que você definiu para a chave.

Com estes secrets e o ambiente configurado, as pipelines de CI/CD estarão prontas para uso.

