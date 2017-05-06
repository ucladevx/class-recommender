import React from 'react';
import {connect} from 'react-redux';


class Contact extends React.Component {
  render(){
    return <div>
      Contact<br/>
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


Contact = connect(mapStateToProps, mapDispatchToProps)(Contact);
export default Contact
