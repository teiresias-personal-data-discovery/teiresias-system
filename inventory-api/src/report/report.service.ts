import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';

import { Report } from './report.model';

@Injectable()
export class ReportService {
  constructor(
    @InjectModel('Report')
    private readonly reportModel: Model<Report>,
  ) {}
  async getReport(query: any) {
    try {
      const reports = await this.reportModel
        .find({})
        .sort({ date: -1 })
        .limit(20);
      return reports;
    } catch {
      throw new InternalServerErrorException();
    }
  }
}
const config = {
  Config: {
    AWS: {
      selected_buckets: [],
      percentage_of_scanned_objects: 100,
    },
    GCDLP: {
      selected_buckets: [],
      percentage_of_scanned_objects: 100,
      should_use_sample_of_each_scanned_object: false,
    },
  },
};
