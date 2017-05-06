import React from 'react';
import {connect} from 'react-redux';
import "bootstrap-sass";



class Account extends React.Component {
  render(){
    return <div>
      Account<br/>
      Path: {this.props.urlPath}
    </div>;
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
