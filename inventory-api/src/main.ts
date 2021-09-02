import 'dotenv/config';
import * as helmet from 'helmet';
import { NestFactory } from '@nestjs/core';
import * as fs from 'fs';

import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {});
  app.use(helmet());
  await app.listen(3001);
}
bootstrap();
