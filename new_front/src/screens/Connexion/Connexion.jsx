// import React from "react";
// import { Link } from "react-router-dom";
// import "./style.css";
//
//
// import { useEffect, useState } from "react";
// import {Link, useNavigate} from "react-router-dom";
// import axios from "axios";
// import UserContext from "../../context/useContext";
// import BaseUrl from "../../config/baseUrl";
// import Swal from "sweetalert2";
//
// const url = BaseUrl();
//
// export const Connexion = () => {
//
//   const user = UserContext();
//
// const [isAuthToken, setIsAuthToken] = useState(localStorage.getItem('_token_ucl'));
// const [msgerrorAlert,setMsgerrorAlert] = useState('');
// const navigate = useNavigate();
//
// const [loginData,setLoginData] = useState({
//     'email':'',
//     'password':''
// });
//
// useEffect(()=>{
//     if(isAuthToken !== null){
//       if(user && user.is_responsable){
//         navigate('/dashboard-/');
//       }
//
//       if(user && user.is_adg){
//         navigate('/dashboard-3/');
//       }
//
//     }
// },[isAuthToken,user]);
//
// const handleChange=(event)=>{
//     setLoginData({
//         ...loginData,
//         [event.target.name] : event.target.value
//     });
// }
//
// const submitLogin=()=>{
//      setMsgerrorAlert('');
//     if(loginData.email !== "" && loginData.password !==""){
//         const _formData = new FormData();
//         _formData.append('email',loginData.email);
//         _formData.append('password',loginData.password);
//
//         try {
//             axios.post(url+'/login/',_formData).then((resp)=>{
//                 if(resp.data.bool == true){
//                     localStorage.setItem('_token_ucl',resp.data.token);
//                     Swal.fire({
//                         title: 'Connexion...',
//                         html: 'Veillez patientez...',
//                         allowEscapeKey: false,
//                         allowOutsideClick: false,
//                         didOpen: () => {
//                           Swal.showLoading()
//                         },
//                     });
//
//                   /*   if(resp.data.role == "superadmin"){
//                       //localStorage.setItem('_token_ucl',resp.data.token);
//                       navigate('/dashboard/');
//                     } */
//
//                     if(resp.data.role == "responsable"){
//                       //localStorage.setItem('_token_ucl',resp.data.token);
//
//                       if(resp.data.proj){
//                         navigate('/dashboard-3/');
//                         window.location.reload();
//                       }else{
//                         navigate('/dashboard-3/');
//                         window.location.reload();
//                       }
//
//                     }
//
//                     if (resp.data.role == "adg"){
//                         navigate('/dashboard-3/');
//                         window.location.reload();
//                     }
//
//                 }else{
//                   setMsgerrorAlert(resp.data.msg);
//                 }
//             })
//         } catch (error) {
//             console.log(error);
//         }
//
//     }
//
//    // console.log(loginData.email)
// }
//
//   return (
//     <div className="connexion row">
//       <div className="group-wrapper-2 col-lg-8">
//         <div className="group-30">
//           <div className="frame">
//             <img className="unknown" alt="Unknown" src="/img/unknown-1.png" />
//             <div className="frame-wrapper">
//               <div className="frame-2">
//                 <div className="group-31">
//                   <div className="text">Connectez-vous</div>
//                   <p className="text-2">Connectez-vous pour accéder à votre espace</p>
//                 </div>
//                 {msgerrorAlert !=="" &&
//                   <div className="alert alert-danger" role="alert">
//                       <h4 className="alert-heading text-center">Attention !</h4>
//                       <p>{msgerrorAlert}</p>
//                   </div>
//                 }
//                 <div className="group-32">
//                   <input
//                       className="overlap-group-5 form-control form-icon-input"
//                       id="email"
//                       type="email"
//                       placeholder="Adresse Email"
//                       name="email"
//                       onChange={handleChange}
//                   />
//                   <div className="text-4">Adresse Email</div>
//                 </div>
//                 <div className="group-32">
//                     <input
//                           className="overlap-group-5 form-control form-icon-input"
//                           id="password"
//                           type="password"
//                           name="password"
//                           placeholder="Mot de Passe"
//                           onChange={handleChange}
//                     />
//                   <div className="text-6">Mot de passe</div>
//                 </div>
//                 <button  className="btn w-100 mb-3" style={{padding: "10px", borderRadius: "32px", fontWeight: "bold", fontSize: "26px", backgroundColor:"#94A91B", color:"white"}} onClick={submitLogin}>Connexion</button>
//               </div>
//             </div>
//           </div>
//           <img className="rectangle-13 img-responsive" alt="Rectangle" src="/img/rectangle-1-1.png" />
//         </div>
//       </div>
//     </div>
//   );
// };



import React from "react";
import { Link } from "react-router-dom";
import "./style.css";
import { useEffect, useState } from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import UserContext from "../../context/useContext";
import BaseUrl from "../../config/baseUrl";
import Swal from "sweetalert2";

const url = BaseUrl();

export const Connexion = () => {
      const user = UserContext();

      const [isAuthToken, setIsAuthToken] = useState(localStorage.getItem('_token_ucl'));
      const [msgerrorAlert,setMsgerrorAlert] = useState('');
      const navigate = useNavigate();

      const [loginData,setLoginData] = useState({
          'email':'',
          'password':''
      });

      useEffect(()=>{
          if(isAuthToken !== null){
            if(user && user.is_responsable){
              navigate('/dashClient/');
            } else if(user && user.is_client) {
              navigate('/dashClient/');
            }

            if(user && user.is_adg){
              navigate('/dashboard-3/');
            }

          }
      },[isAuthToken,user]);

      const handleChange=(event)=>{
          setLoginData({
              ...loginData,
              [event.target.name] : event.target.value
          });
      }

      const submitLogin=()=>{
          setMsgerrorAlert('');
          if(loginData.email !== "" && loginData.password !==""){
              const _formData = new FormData();
              _formData.append('email',loginData.email);
              _formData.append('password',loginData.password);

              try {
                  axios.post(url+'/login/',_formData).then((resp)=>{
                      if(resp.data.bool == true){
                          localStorage.setItem('_token_ucl',resp.data.token);
                          Swal.fire({
                              title: 'Connexion...',
                              html: 'Veillez patientez...',
                              allowEscapeKey: false,
                              allowOutsideClick: false,
                              didOpen: () => {
                                Swal.showLoading()
                              },
                          });

                        /*   if(resp.data.role == "superadmin"){
                            //localStorage.setItem('_token_ucl',resp.data.token);
                            navigate('/dashboard/');
                          } */

                          if(resp.data.role == "responsable"){
                            //localStorage.setItem('_token_ucl',resp.data.token);

                            if(resp.data.proj){
                              navigate('/dashClient/');
                              window.location.reload();
                            }else{
                              navigate('/dashClient/');
                              window.location.reload();
                            }

                          }

                          if(resp.data.role == "client"){
                            //localStorage.setItem('_token_ucl',resp.data.token);

                            if(resp.data.proj){
                              navigate('/dashClient/');
                              window.location.reload();
                            }else{
                              navigate('/dashClient/');
                              window.location.reload();
                            }

                          }

                          if (resp.data.role == "adg"){
                              navigate('/dashboard-3/');
                              window.location.reload();
                          }

                      }else{
                        setMsgerrorAlert(resp.data.msg);
                      }
                  })
              } catch (error) {
                  console.log(error);
              }

          }

        // console.log(loginData.email)
      }

  return (
    <div className="connexion row">
      <div className="div-8 col-lg-8">
        <div className="group-24">
          <div className="overlap-16">
            <div className="group-25">
              <input
                  className="overlap-group-5 form-control form-icon-input"
                  id="email"
                  type="email"
                  placeholder="Adresse Email"
                  name="email"
                  onChange={handleChange}
              />
              <div className="text-2">Email</div>
            </div>
            <div className="group-26">
                <input
                      className="overlap-group-5 form-control form-icon-input"
                      id="password"
                      type="password"
                      name="password"
                      placeholder="Mot de Passe"
                      onChange={handleChange}
                />
              <div className="text-3">Mot de passe</div>
            </div>
            <div className="group-27">
              <div className="text-4">Connectez-vous</div>
              <p className="text-5">Connectez-vous pour accéder à votre espace</p>
            </div>
            <button
                className="group-28"
                style={{
                    padding: "10px",
                    borderRadius: "32px",
                    fontWeight: "bold",
                    fontSize: "26px",
                    backgroundColor:"#94A91B",
                    color:"white"
                }}
                onClick={submitLogin}>
                    Connexion
            </button>
            <div className="group-27">
               {msgerrorAlert !=="" &&
//                   <div className="alert alert-danger" role="alert">
//                       <h4 className="text-5 alert-heading text-center">Attention !</h4>
//                       <p>{msgerrorAlert}</p>
//                   </div>
                  <div className="group-5 alert alert-danger" role="alert" style={{marginTop: "20px"}}>
                      <p className="text-6 text-5 alert-heading text-center" style={{marginTop: "8px", fontWeight: "14px", textAlign:"center"}}>
                          {msgerrorAlert}
{/*                           Attention, erreurs d’identification veuillez réessayer */}
                      </p>
                      <img className="vector" style={{marginTop: "8px", fontWeight: "14px"}} alt="Vector" src="/img/vector.svg" />
                  </div>
               }
            </div>
{/*             <Link className="group-28" to="/dashboard-3"> */}
{/*               <div className="overlap-17"> */}
{/*                 <div className="text-6">Connexion</div> */}
{/*               </div> */}
{/*             </Link> */}
          </div>
          <img className="unknown" alt="Unknown" src="/img/unknown-1.png" />
        </div>
        <div className="col-lg-4">
            <img className="rectangle-7 col-lg-4" alt="Rectangle" src="/img/rectangle-1-1.png" />
        </div>
      </div>
    </div>
  );
};
