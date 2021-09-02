import { Controller, Get, Request, UseGuards } from '@nestjs/common';

import { ReportService } from './report.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('report')
export class ReportController {
  constructor(private reportService: ReportService) {}

  @UseGuards(JwtAuthGuard)
  @Get()
  async getReport(@Request() req) {
    return await this.reportService.getReport(req);
  }
}
