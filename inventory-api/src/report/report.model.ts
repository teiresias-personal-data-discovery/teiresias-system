import { Schema } from 'mongoose';
import { Document } from 'mongoose';

export const ReportSchema = new Schema(
  {
    trigger: String,
    details: Schema.Types.Mixed,
  },
  { timestamps: true },
);

export interface Report extends Document {
  id: string;
  createdAt: string;
  updatedAt: string;
  trigger: string;
  details: {};
}
