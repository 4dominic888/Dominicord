const mongoose = require("mongoose");
const palabraDiSchema = new mongoose.Schema({
    username: {type: String, require: true},
    profilePhoto : {type: String, require: true},
    palabra: {type: String, require: true, unique: true},
    descripcion: {type: String, require: true}
});
const model = mongoose.model("palabrasDi", palabraDiSchema);
module.exports = model;