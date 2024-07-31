// // passport.js

// const passport = require('passport');
// const GoogleStrategy = require('passport-google-oauth20').Strategy;
// const MicrosoftStrategy = require('passport-microsoft').Strategy;
// const AppleStrategy = require('passport-apple').Strategy;

// // Google OAuth configuration
// passport.use(new GoogleStrategy({
//     clientID: process.env.GOOGLE_CLIENT_ID,
//     clientSecret: process.env.GOOGLE_CLIENT_SECRET,
//     callbackURL: '/auth/google/callback'
//   },
//   (accessToken, refreshToken, profile, done) => {
//     // User.findOrCreate({ googleId: profile.id }, (err, user) => {
//     //   return done(err, user);
//     // });
//     return done(null, profile);
//   }
// ));

// // Microsoft OAuth configuration
// passport.use(new MicrosoftStrategy({
//     clientID: process.env.MICROSOFT_CLIENT_ID,
//     clientSecret: process.env.MICROSOFT_CLIENT_SECRET,
//     callbackURL: '/auth/microsoft/callback',
//     scope: ['user.read']
//   },
//   (accessToken, refreshToken, profile, done) => {
//     // User.findOrCreate({ microsoftId: profile.id }, (err, user) => {
//     //   return done(err, user);
//     // });
//     return done(null, profile);
//   }
// ));

// // Apple OAuth configuration
// passport.use(new AppleStrategy({
//     clientID: process.env.APPLE_CLIENT_ID,
//     teamID: process.env.APPLE_TEAM_ID,
//     keyID: process.env.APPLE_KEY_ID,
//     privateKeyString: process.env.APPLE_PRIVATE_KEY,
//     callbackURL: '/auth/apple/callback'
//   },
//   (accessToken, refreshToken, idToken, profile, done) => {
//     // User.findOrCreate({ appleId: idToken.sub }, (err, user) => {
//     //   return done(err, user);
//     // });
//     return done(null, profile);
//   }
// ));

// // Serialize user into the sessions
// passport.serializeUser((user, done) => {
//   done(null, user);
// });

// // Deserialize user from the sessions
// passport.deserializeUser((obj, done) => {
//   done(null, obj);
// });

// module.exports = passport;
