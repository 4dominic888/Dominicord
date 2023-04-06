const mongoose = require("mongoose");
const memeSchema = new mongoose.Schema({
    username: {type: String, require: true},
    memeURL: {type: String, require: true},
    memeName: {type: String, require: true}
});
const model = mongoose.model("MemesEnviados", memeSchema);
module.exports = model;