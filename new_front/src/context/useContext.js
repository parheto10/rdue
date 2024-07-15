import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import BaseUrl from "../config/baseUrl";

// const baseUrl = 'http://127.0.0.1:8000/api';
const url = BaseUrl();


function UserContext(){
    //const [isAuthToken, setIsAuthToken] = useState(localStorage.getItem('_token_ucl'));
    const [user,setUsers] = useState(null);
    const navigate = useNavigate();

    useEffect(()=>{
       
        if(localStorage.getItem('_token_ucl') !== null){
            try {
                axios.get(url+'/users-clients/?token='+localStorage.getItem('_token_ucl'),{
                    headers:{
                        'Content-Type':'application/json'
                    },
                    credentials:'include'
                }).then((resp)=>{   
                    if(resp.data.length == 0){  
                        //setIsAuthToken(null);
                        setUsers(null);
                        localStorage.removeItem('_token_ucl');
                        navigate('/');
                    }else{
                        setUsers(resp.data[0]);
                    }
                   
                })
            } catch (error) {
                console.log(error);
            }
        }

        if(localStorage.getItem('_token_ucl') == null){
            localStorage.removeItem('_token_ucl');
            navigate('/');
        }

    },[]);




    return user;

}

export default UserContext;