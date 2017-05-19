import React from 'react';
import {connect} from 'react-redux';


class AccountForm extends React.Component {
  render(){
    return( 
      <div>
        <form>
          Name:
          <input className = "accountFormInput" type="text"/>
        </form>
      </div>
      );
  }
}

export default AccountForm
