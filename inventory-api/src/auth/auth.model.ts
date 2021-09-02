import { Schema } from 'mongoose';
import { Document } from 'mongoose';

export const UserSchema = new Schema({
  userName: String,
  pwdHash: String,
  salt: String,
});

export interface User extends Document {
  id: string;
  userName: string;
  pwdHash: string;
}

export interface TokenPayload {
  userName: string;
}

export class LoginDTO {
  userName: string;
  pwd: string;
}
