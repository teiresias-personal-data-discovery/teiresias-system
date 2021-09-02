import {
  Injectable,
  BadRequestException,
  InternalServerErrorException,
} from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { JwtService } from '@nestjs/jwt';

import { Model } from 'mongoose';
import * as bcrypt from 'bcryptjs';

import { LoginDTO, User } from './auth.model';

@Injectable()
export class AuthService {
  constructor(
    @InjectModel('User')
    private readonly userModel: Model<User>,
    private jwtService: JwtService,
  ) {}
  async login({ userName, pwd }: LoginDTO) {
    let user;
    try {
      user = await this.userModel.findOne({
        userName,
      });
    } catch {
      throw new InternalServerErrorException();
    }
    if (user && bcrypt.compareSync(pwd, user.pwdHash)) {
      const token = this.jwtService.sign({ userName });
      return { userName, token };
    }

    throw new BadRequestException('Credentials invalid');
  }
}
