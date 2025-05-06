## Run locally

### 1. Clone the Repository

Start by cloning the **LittleX** repository to your local system:

```bash
git clone https://github.com/Jaseci-Labs/littleX.git
cd littlex
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Create Cluster
```bash
kind create cluster --name littlex --config kind-config.yaml
```
### 4. Initialize Jac-splice-orc
```bash
jac orc_initialize littlex
```
### 5. Set OpenAI API Key

- For linux
```bash
export OPENAI_API_KEY='your-open-api-key'
```
- For Windows
```bash
set OPENAI_API_KEY='your-open-api-key'
```

### 6. Start the Backend Server
- Run littleX_mini
```bash
jac serve littleX_BE/littleX_mini.jac
```
- Run littleX_full
```bash
jac serve littleX_BE/littleX_full.jac
```
### 7. Run the Frontend Server
Open another command line
```bash
cd littleX_FE
npm i
npm run dev
```


