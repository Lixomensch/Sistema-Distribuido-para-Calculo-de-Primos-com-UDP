# Sistema Distribuído para Cálculo de Números Primos com UDP

Este projeto implementa um sistema cliente-servidor utilizando sockets UDP para encontrar números primos de forma distribuída. O servidor divide um intervalo numérico em subintervalos, e os clientes solicitam tarefas, processam os números primos e enviam os resultados de volta.

## Estrutura do Projeto

- `server.py` - Servidor que distribui tarefas e agrega os resultados.
- `client.py` - Cliente que solicita tarefas, calcula números primos e envia os resultados.
- `primes.txt` - Arquivo gerado pelo servidor contendo os números primos encontrados.
- `tests/` - Diretório contendo testes automatizados para a comunicação entre cliente e servidor.

## Requisitos

- Python 3.8 ou superior
- `make` instalado no sistema (somente para testes)

## Como Executar

### 1. Iniciar o Servidor

Execute o seguinte comando para iniciar o servidor:

```bash
python server.py
```

### 2. Iniciar os Clientes

Abra outro terminal e execute um ou mais clientes:

```bash
python client.py
```

Os clientes solicitarão tarefas ao servidor, calcularão os números primos e enviarão os resultados.

### 3. Finalização

O servidor encerrará automaticamente após processar todo o intervalo e salvará os resultados em `primes.txt`.

## Protocolo de Comunicação

A comunicação entre cliente e servidor ocorre via JSON no seguinte formato:

- **Cliente → Servidor:** `{"type": "request"}`
- **Servidor → Cliente:** `{"type": "task", "range": [inicio, fim]}` ou `{"type": "done"}`
- **Cliente → Servidor:** `{"type": "result", "primes": [lista de primos]}`

## Testes

O projeto inclui testes automatizados para validar a comunicação entre servidor e cliente, além do processamento correto dos números primos.

### Executando os Testes com Make

Para rodar os testes, utilize os seguintes comandos:

- **Testar um único cliente:**

  ```bash
  make one
  ```

- **Testar múltiplos clientes:**

  ```bash
  make multiple
  ```

- **Testar a função de verificação de primos:**
  ```bash
  make isPrime
  ```

### Cobertura dos Testes

- **Distribuição de Tarefas pelo Servidor:** Garante que o servidor atribui corretamente os intervalos de números aos clientes.
- **Comunicação Cliente-Servidor:** Valida a troca de mensagens entre o cliente e o servidor.
- **Cálculo de Números Primos:** Testa se os clientes calculam corretamente os números primos nos intervalos atribuídos.
- **Agregação de Resultados:** Verifica se o servidor recebe e armazena corretamente os números primos enviados pelos clientes.

## Autor

João Pedro Lemes Queiroz

## Licença

Este projeto é de uso educacional.
