import Ajv from "ajv";
import { prettify } from "awesome-ajv-errors";
import fs from "node:fs/promises";
import path from "node:path";

const args = process.argv.slice(2);
const type = args[0];

const ajv = new Ajv({ strict: false });

try
{
    // Define custom formats
    ajv.addFormat('url_safe', /^[a-z0-9\-\_]*$/gi)

    // Load json + schema
    const jsonRaw = await fs.readFile(path.resolve(`./data/${type}.json`), "utf8");
    const schemaRaw = await fs.readFile(path.resolve(`./schemas/${type}.schema.json`), "utf8");

    const json = JSON.parse(jsonRaw);
    const schema = JSON.parse(schemaRaw);

    // Validate the json against the schema
    const validate = ajv.compile(schema);
    const isValid = validate(json);

    // Output the message
    if (!isValid) {
        console.log(`${type}.json is invalid`);
        console.error(prettify(validate, { data: json }));
        process.exit(1);
    } else {
        // You don't need to print anything when it passes.
    }
} 
catch (err) 
{
    console.error(err.message);
    process.exit(1);
}