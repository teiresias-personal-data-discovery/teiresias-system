import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

import { AuthModule } from './auth/auth.module';
import { ReportModule } from './report/report.module';

const baseConnectionString = () => {
  switch (process.env.NODE_ENV) {
    case 'production':
      return `mongodb://${process.env.MONGO_INVENTORYAPI_USERNAME}:${process.env.MONGO_INVENTORYAPI_PASSWORD}@host.docker.internal`;
    default:
      return `mongodb://${process.env.MONGO_INVENTORYAPI_USERNAME}:${process.env.MONGO_INVENTORYAPI_PASSWORD}@localhost`;
  }
};

@Module({
  imports: [
    MongooseModule.forRoot(`${baseConnectionString()}/userData`, {
      connectionName: 'userData',
    }),
    MongooseModule.forRoot(
      `${baseConnectionString()}/${process.env.MONGO_INVENTORY_DATABASE}`,
      {
        connectionName: process.env.MONGO_INVENTORY_DATABASE,
      },
    ),
    AuthModule,
    ReportModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
