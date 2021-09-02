import { Body, Controller, Post } from '@nestjs/common';
import { LoginDTO } from './auth.model';
import { AuthService } from './auth.service';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}
  @Post()
  login(@Body() credentials: LoginDTO) {
    return this.authService.login(credentials);
  }
}
