export const labels = {
    // PARSER
    parserTitle: "This is Parser",
    parserStep1: "Parser Step 1: -> upload MD file => parser returns Excel with quotes",
    parserStep2: "Parser Step 2: -> upload MD file and Excel with quotes file => parser returns MD parsed file",
    replaceTranslationsTitle: "Replace Translations -> MD",

    // TRANSLATOR
    translatorTitle: "This is Translator",
    translatorStep1: "Translator Step 1: -> upload MD (book upload), you can upload more than one book",
    translatorStep2: "Translator Step 2: -> select a book from the list of uploaded books",
    translatorStep3: "Translator Step 3: -> select chapters to translate",
    translatorStep4: "Translator Step 4: -> upload Excel",
    translatorStep5: "Translator Step 5: -> submit and wait till enp of process => download md book",
    translationCompleted: "Translation completed",
    translationExpiredMessage: "Translation expired after 1 hour",
    eventSource: "Event source",

    // DASHBOARD
    instruction: "Instruction",
    parser: "Parser",
    translator: "Translator",
    instructionDescription: "How to use the tools",

    // FILE
    chooseFile: "Choose file: ",
    quoteType: "Quotation type: ",
    choose: "Selected: ",
    chooseBookTitle: "Choose book title",
    chooseExcelFile: "Choose Excel file (.xlsx):",
    chooseMarkdownFile: "Choose Markdown file (.md):",
    fileDeleted: "File deleted",
    beforeDeleteFileAlert: "Did the download complete successfully? Click OK to delete the file from the server.",

    // ACTIONS
    processing: "Processing...",
    sendMDAndReceivedExcel: "Send MD and download XLSX",
    sendMDAndExcelReceivedMD: "Send MD and XLSX download MD",
    downloadTranslatedBook: "Download translated book",

    // CHAPTERS
    selectAllChapters: "Select all chapters",
    sendSelection: "Send selection",
    successMessagePrefix: "Success:",
    errorMessagePrefix: "Error:",
    chooseChapterTitle: "Choose chapters",
    confirmChaptersSelection: "Confirm chapters selection",

    // BOOK
    bookAndChaptersSelectionToTranslationTitle: "Select Book and Chapters to translate",
    loadingBook: "Loading book...",
    bookErrorPrefix: "Error:",
    bookNotFound: "No book data available.",
    bookTitleLabel: "Title:",
    bookAuthorLabel: "Author:",
    bookDescriptionLabel: "Description:",
    bookIdLabel: "Book ID:",
    fetchBookButton: "Fetch book",
    getBookByIdTitle: "Get Book by ID",
    bookQuotationLabel: "Quotation type:",
    getBookLabelTitle: "Get Book by ID",
    uploadBookTitle: "Upload book for translation",
    bookGenreLabel: "Genre:",
    bookQuoteTypeLabel: "Quotation type:",
    bookFileLabel: "Excel file (.xlsx):",
    bookUploadButton: "Upload book",
    bookUploading: "Uploading...",
    bookUploadErrorPrefix: "Error:",
    bookList: "Book list",
    emptyBookList: "No books available",
    id: "ID",
    title: "Title ",
    bookGenre: "Book Genre ",
    uploadExcelFileWithQuoteToTranslationTitle: "Upload Excel file with quotes",
    sendBookToTranslation: "Send Book to Translation",
} as const;
