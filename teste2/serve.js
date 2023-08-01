const express = require('express');
const cors = require('cors');
const app = express();
const fs = require('fs');
const PDFParser = require('pdf-parse');
const path = require('path');
const mysql = require('mysql2');

class Pdf {
  static async getPDFText(source) {
    const pdfData = await PDFParser(source);
    return pdfData.text;
  }
}

app.use(cors());
app.use(express.json());

app.get('/ping', (req, res) => res.send('pong'));

app.get('/file/:filename', async (req, res) => {
  const folderPath = path.join(__dirname, 'Faturas');
  const filePath = path.join(folderPath, req.params.filename);

  if (!fs.existsSync(filePath)) {
    res.status(404).send('Arquivo não encontrado');
    return;
  }

  const fileBuffer = fs.readFileSync(filePath);
  const pdfText = await Pdf.getPDFText(fileBuffer); // Usando a classe Pdf para extrair o texto do PDF

  res.json({ filename: req.params.filename, text: pdfText });
});

app.get('/files', (req, res) => {
  const folderPath = path.join(__dirname, 'Faturas');
  const files = fs.readdirSync(folderPath).filter(file => file.endsWith('.pdf'));
  res.json(files);
});

app.get('/index.html', (req, res) => {
    const indexPath = path.join(__dirname, 'index.html');
    res.sendFile(indexPath);
  });


  // Rota para inserir os dados no banco de dados MySQL
app.post('/insert-data', async (req, res) => {
    const pdfData = req.body.pdfData; // Supondo que os dados do PDF estão em req.body.pdfData
  
    // Configuração da conexão com o banco de dados MySQL
    const connection = mysql.createConnection({
      host: 'localhost',
      user: 'root',
      password: '12345',
      database: 'faturas'
    });
  
    try {
      // Estabelecer a conexão com o banco de dados
      await connection.promise().query('USE faturas');
  
      // Inserir os dados no banco de dados (substitua "sua_tabela" pelo nome da tabela que você deseja usar)
      const result = await connection.promise().query('INSERT INTO faturas (conteudo_pdf) VALUES (?)', [pdfData]);
      console.log('Dados inseridos no banco de dados com sucesso:', result);
  
      res.status(200).send('Dados inseridos no banco de dados com sucesso');
    } catch (error) {
      console.error('Erro ao inserir dados no banco de dados:', error);
      res.status(500).send('Erro ao inserir dados no banco de dados');
    } finally {
      // Fechar a conexão com o banco de dados
      connection.end();
    }
  });
  
  


const PORT = 3333;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
