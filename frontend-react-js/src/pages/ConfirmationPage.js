import './ConfirmationPage.css';
import React from "react";
import { useParams, useSearchParams } from 'react-router-dom';
import {ReactComponent as Logo} from '../components/svg/logo.svg';

import { Auth } from 'aws-amplify';

export default function ConfirmationPage() {
  const [email, setEmail] = React.useState('');
  const [code, setCode] = React.useState('');
  const [codeSent, setCodeSent] = React.useState(false);
  const [cognitoErrors, setCognitoErrors] = React.useState('');
  const [searchParams] = useSearchParams()

  const code_onchange = (event) => {
    setCode(event.target.value);
  }
  const email_onchange = (event) => {
    setEmail(event.target.value);
  }

  const resend_code = async (event) => {
    console.log('resend_code')
    setCognitoErrors('')

    try {
      await Auth.resendSignUp(email)
      console.log('code resent successfully')
      setCodeSent(true)
    } catch(error) {
        console.log(error)
        if (error.message == 'Username cannot be empty') {
          setCognitoErrors("You need to provide an email in order to resend the activation code")
        } else if (error.message == "Username/client id combination not found.") {
          setCognitoErrors("Email is invalid or cannot be found")
        }
    }
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    setCognitoErrors('')
    try {
      await Auth.confirmSignUp(email, code);
      window.location.href = "/"
    } catch(error) {
      setCognitoErrors(error.message)
    }
    return false
  }

  let errors;
  if (cognitoErrors){
    errors = <div className='errors'>{cognitoErrors}</div>;
  }


  let code_button;
  if (codeSent){
    code_button = <div className="sent-message">A new activation code has been sent to your email</div>
  } else {
    code_button = <button className="resend" onClick={resend_code}>Resend Activation Code</button>;
  }

  React.useEffect(()=>{
    if (searchParams.get('email')) {
      setEmail(searchParams.get('email'))
    }
  }, [])

  return (
    <article className="confirm-article">
      <div className='recover-info'>
        <Logo className='logo' />
      </div>
      <div className='recover-wrapper'>
        <form
          className='confirm_form'
          onSubmit={onsubmit}
        >
          <h2>Confirm your Email</h2>
          <div className='fields'>
            <div className='field text_field email'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange} 
              />
            </div>
            <div className='field text_field code'>
              <label>Confirmation Code</label>
              <input
                type="text"
                value={code}
                onChange={code_onchange} 
              />
            </div>
          </div>
          {errors}
          <div className='submit'>
            <button type='submit'>Confirm Email</button>
          </div>
        </form>
      </div>
      {code_button}
    </article>
  );
}