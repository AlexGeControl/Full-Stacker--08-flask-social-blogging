/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://localhost:50080/api/v2', // the running FLASK api server url inside docker-compose
  auth0: {
    url: 'dev-d-and-g-udaspicelatte', // the auth0 domain prefix
    audience: 'drinks', // the audience set for the auth0 app
    clientId: 'ZolXEl6eVCUQNU8N7BzIgppmdSIoLgj4', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:58100', // the base url of the running ionic application. 
  }
};
