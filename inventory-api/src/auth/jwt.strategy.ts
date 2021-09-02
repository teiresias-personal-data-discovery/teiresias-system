import {
  Injectable,
  UnauthorizedException,
  InternalServerErrorException,
} from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { PassportStrategy } from '@nestjs/passport';

import { Model } from 'mongoose';
import { ExtractJwt, Strategy } from 'passport-jwt';

import { User, TokenPayload } from './auth.model';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    @InjectModel('User')
    private readonly userModel: Model<User>,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.JWT_SECRET,
    });
  }

  async validate({ userName }: TokenPayload) {
    try {
      const users = await this.userModel.find({
        userName,
      });
      if (!users.length) {
        throw new UnauthorizedException();
      }
      return userName;
    } catch {
      throw new InternalServerErrorException();
    }
  }
}
