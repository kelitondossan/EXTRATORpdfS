const pdfjslib = require('pdfjs-dist/es5/build/pdf')
const cors = require('cors');

class Pdf {
  static async getPageText (pdf, pageNo) {
    const page = await pdf.getPage(pageNo)
    const tokenizedText = await page.getTextContent()

    const pageText = tokenizedText.items.map(token => token.str).join('')
    return pageText
  }

  static async getPDFText (source, password) {
    const pdf = await pdfjslib.getDocument({ data: source, password }).promise
    const maxPages = pdf.numPages

    const pageTextPromises = []
    for (let pageNo = 1; pageNo <= maxPages; pageNo += 1) {
      pageTextPromises.push(Pdf.getPageText(pdf, pageNo))
    }
    const pageTexts = await Promise.all(pageTextPromises)
    return pageTexts.join(' ')
  }
}

module.exports = Pdf