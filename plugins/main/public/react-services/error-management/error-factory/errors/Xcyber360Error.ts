import { IXcyber360Error, IXcyber360ErrorInfo, IXcyber360ErrorLogOpts } from "../../types";


export default abstract class Xcyber360Error extends Error {
    abstract logOptions: IXcyber360ErrorLogOpts;
    constructor(public error: Error, info?: IXcyber360ErrorInfo) {
        super(info?.message || error.message);
        const childrenName = this.constructor.name; // keep the children class name
        Object.setPrototypeOf(this, Xcyber360Error.prototype); // Because we are extending built in class
        this.name = childrenName;
        this.stack = this.error.stack; // keep the stack trace from children
    }
}