import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const DashboardScreen = () => {
  return (
    <div className="dashboard-screen">
      <div className="dashboard-2">
        <div className="rectangle-8" />
        <div className="overlap-18">
          <div className="group-29">
            <div className="overlap-group-6">
              <img className="vector-12" alt="Vector" src="/img/vector.png" />
              <div className="ellipse-6" />
            </div>
          </div>
          <div className="group-30">
            <div className="overlap-19">
              <img className="vector-13" alt="Vector" src="/img/vector-1.png" />
              <div className="ellipse-7" />
            </div>
          </div>
        </div>
        <div className="overlap-20">
          <div className="enregistrement-d-un-wrapper">
            <div className="enregistrement-d-un">Enregistrement d&#39;un producteur</div>
          </div>
          <div className="overlap-21">
            <div className="text-wrapper-23">Rechercher ici...</div>
          </div>
          <div className="overlap-22">
            <div className="text-wrapper-23">Rechercher ici...</div>
          </div>
          <div className="overlap-23">
            <div className="text-wrapper-23">Rechercher ici...</div>
          </div>
          <div className="overlap-24">
            <div className="text-wrapper-23">Rechercher ici...</div>
          </div>
          <div className="overlap-25">
            <div className="text-wrapper-23">Rechercher ici...</div>
          </div>
          <div className="overlap-26">
            <div className="text-wrapper-23">Rechercher ici...</div>
          </div>
          <div className="overlap-27">
            <div className="text-wrapper-24">Valider</div>
          </div>
          <div className="overlap-28">
            <div className="overlap-group-7">
              <div className="text-wrapper-25">Choisir une photo</div>
            </div>
            <div className="text-wrapper-26">Aucun fichier choisi...</div>
          </div>
          <div className="text-wrapper-27">Contact</div>
          <div className="text-wrapper-28">Nombre de parcelle</div>
          <div className="text-wrapper-29">Nom complet</div>
          <div className="text-wrapper-30">Section</div>
          <div className="text-wrapper-31">Code du producteur</div>
          <div className="text-wrapper-32">Lieu d’habitation</div>
        </div>
        <div className="group-31" />
        <img className="rectangle-9" alt="Rectangle" src="/img/rectangle-1.png" />
        <div className="rectangle-10" />
        <div className="group-32">
          <div className="text-wrapper-33">RDUE</div>
          <img className="vector-14" alt="Vector" src="/img/vector-18.png" />
        </div>
        <a
          className="group-33"
          href="https://demo.akidompro.com/analyseCOOPAAHS"
          rel="noopener noreferrer"
          target="_blank"
        >
          <div className="text-wrapper-34">Rapport analyse RDUE</div>
          <img className="vector-15" alt="Vector" src="/img/vector-2.png" />
        </a>
        <div className="group-34">
          <div className="text-wrapper-34">Campagnes</div>
          <img className="vector-16" alt="Vector" src="/img/vector-3.png" />
        </div>
        <Link className="group-35" to="/dashboard-4">
          <div className="group-36">
            <img className="group-37" alt="Group" src="/img/group-206.png" />
            <div className="text-wrapper-34">Coopératives</div>
          </div>
        </Link>
        <Link className="group-38" to="/dashboard-3">
          <img className="vector-17" alt="Vector" src="/img/vector-4.png" />
          <div className="text-wrapper-35">Tableau de bord</div>
        </Link>
        <div className="group-39">
          <div className="group-40">
            <div className="overlap-group-8">
              <img className="logo-agro-map-2" alt="Logo agro map" />
              <div className="text-wrapper-36">AKIDOMPRO</div>
            </div>
          </div>
        </div>
        <div className="group-41">
          <div className="text-wrapper-33">Administration</div>
          <img className="vector-18" alt="Vector" src="/img/vector-18-1.png" />
        </div>
        <div className="group-42">
          <div className="text-wrapper-33">Paramètre</div>
          <img className="vector-19" alt="Vector" src="/img/vector-18-2.png" />
        </div>
        <div className="group-43">
          <div className="overlap-29">
            <div className="rectangle-11" />
            <div className="group-44">
              <div className="group-45">
                <div className="text-wrapper-37">Géoportail RDUE</div>
                <img className="vector-15" alt="Vector" src="/img/vector-5.png" />
              </div>
            </div>
          </div>
        </div>
        <Link className="group-46" to="/dashboard-6">
          <div className="text-wrapper-34">Géoportail planning</div>
          <img className="vector-20" alt="Vector" src="/img/vector-6.png" />
        </Link>
        <div className="group-47">
          <div className="text-wrapper-34">Enquête sociale</div>
          <img className="vector-20" alt="Vector" src="/img/vector-6.png" />
        </div>
        <Link className="group-48" to="/dashboard-9">
          <div className="text-wrapper-34">Project</div>
          <img className="vector-21" alt="Vector" src="/img/vector-8.png" />
        </Link>
      </div>
    </div>
  );
};
