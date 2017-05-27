import React from 'react';
import {connect} from 'react-redux';
import AccountForm from './account_form'


class Account extends React.Component {
  render(){
    return( 
      <div className = "accountFormContainer">
        <AccountForm />
      </div>
    );
  }
}

const mapStateToProps = (state)=>{
  return {
    urlPath: state.router.location.pathname,
  };
};

const mapDispatchToProps = (dispatch)=>{
  return {
  };
};


Account = connect(mapStateToProps, mapDispatchToProps)(Account);
export default Account
