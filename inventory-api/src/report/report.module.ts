import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

import { ReportService } from './report.service';
import { ReportController } from './report.controller';
import { ReportSchema } from './report.model';

@Module({
  imports: [
    MongooseModule.forFeature(
      [{ name: 'Report', schema: ReportSchema }],
      process.env.MONGO_INVENTORY_DATABASE,
    ),
  ],
  providers: [ReportService],
  controllers: [ReportController],
})
export class ReportModule {}
