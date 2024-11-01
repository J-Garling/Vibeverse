# Testing Records

## Auth Testing

### Registration

| Test Heading | Test Data | Expected OutCome | Actual Outcome | Result |
| --------------|-----------|-------------------|-------------------|-----------|
| Register Valid User | Username: Samuel, Email: Samuel@gmail.com Password: Bruncker | Account Created | Account Created | Passed |
| Register Duplicate Account | Username: Samuel, Email: Samuel@gmail.com, Password: Bruncker | User name already exists | User name already exists | Passed |
| Password < 8 Chars | Username: Sam, Email: Sam@gmail.com Password: Test | Password must be at least 8 characters long | Password must be at least 8 characters long | Passed |
| Common Password 1 | Username: CommonPassword, Email: Sam@gmail.com Password: password | Password is too common | Password is too common | Passed |
| Common Password 2 | Username: CommonPassword2, Email: Sam@gmail.com Password: 123456 | Password is too common | Password is too common | Passed |



### Login

| Test Heading  | Test Data | Expected OutCome  | Actual Outcome    | Result    |
| --------------|-----------|-------------------|-------------------|-----------|
| Login Valid User | Username: Samuel, Password: Bruncker | User Redirected to home page | User Redirected to home page | Passed |
| Login Non-existent User | Username: Nonexistent, Password: Bruncker | Incorrect user name | Incorrect user name | Passed |
| Login Wrong Password | Username: Samuel, Password: FakePasswd | Incorrect password | Incorrect password | Passed |

