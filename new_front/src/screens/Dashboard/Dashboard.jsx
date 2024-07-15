import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Dashboard = () => {
  return (
    <div className="dashboard">
      <div className="div-7">
        <div className="rectangle-3" />
        <div className="overlap">
          <div className="group-5">
            <div className="overlap-group-3">
              <img className="vector-2" alt="Vector" src="/img/vector.png" />
              <div className="ellipse-4" />
            </div>
          </div>
          <div className="overlap-wrapper">
            <div className="overlap-2">
              <img className="vector-3" alt="Vector" src="/img/vector-1.png" />
              <div className="ellipse-5" />
            </div>
          </div>
        </div>
        <div className="overlap-3">
          <div className="overlap-4">
            <div className="text-wrapper-5">Enregistrement de projet</div>
          </div>
          <div className="overlap-5">
            <div className="text-wrapper-6">Rechercher ici...</div>
          </div>
          <div className="overlap-6">
            <div className="text-wrapper-6">Rechercher ici...</div>
          </div>
          <div className="overlap-7">
            <div className="text-wrapper-7">Rechercher ici...</div>
          </div>
          <div className="overlap-8">
            <div className="text-wrapper-7">Rechercher ici...</div>
          </div>
          <div className="overlap-9">
            <div className="text-wrapper-7">Rechercher ici...</div>
          </div>
          <div className="overlap-10">
            <div className="text-wrapper-7">Rechercher ici...</div>
          </div>
          <div className="overlap-11">
            <div className="text-wrapper-6">Rechercher ici...</div>
          </div>
          <div className="overlap-12">
            <div className="text-wrapper-6">Rechercher ici...</div>
          </div>
          <div className="overlap-13">
            <div className="text-wrapper-6">Rechercher ici...</div>
          </div>
          <div className="overlap-14">
            <div className="text-wrapper-8">Valider</div>
          </div>
          <div className="text-wrapper-9">Description du projet</div>
          <div className="text-wrapper-10">Date de fin</div>
          <div className="text-wrapper-11">Objectifs</div>
          <div className="text-wrapper-12">Plants à produire</div>
          <div className="text-wrapper-13">Objectifs</div>
          <div className="text-wrapper-14">Objectifs</div>
          <div className="text-wrapper-15">Date de début</div>
          <div className="text-wrapper-16">Pays</div>
          <div className="text-wrapper-17">Nom du projet</div>
        </div>
        <div className="group-6" />
        <img className="rectangle-4" alt="Rectangle" src="/img/rectangle-1.png" />
        <div className="rectangle-5" />
        <div className="group-7">
          <div className="text-wrapper-18">RDUE</div>
          <img className="vector-4" alt="Vector" src="/img/vector-18.png" />
        </div>
        <a
          className="group-8"
          href="https://demo.akidompro.com/analyseCOOPAAHS"
          rel="noopener noreferrer"
          target="_blank"
        >
          <div className="text-wrapper-19">Rapport analyse RDUE</div>
          <img className="vector-5" alt="Vector" src="/img/vector-2.png" />
        </a>
        <div className="group-9">
          <div className="text-wrapper-19">Campagnes</div>
          <img className="vector-6" alt="Vector" src="/img/vector-3.png" />
        </div>
        <Link className="group-10" to="/dashboard-4">
          <div className="group-11">
            <img className="group-12" alt="Group" src="/img/group-206.png" />
            <div className="text-wrapper-19">Coopératives</div>
          </div>
        </Link>
        <Link className="group-13" to="/dashboard-3">
          <img className="vector-7" alt="Vector" src="/img/vector-4.png" />
          <div className="text-wrapper-20">Tableau de bord</div>
        </Link>
        <div className="group-14">
          <div className="group-15">
            <div className="overlap-group-4">
              <img className="logo-agro-map" alt="Logo agro map" src="/img/logo-agro-map-1.png" />
              <div className="text-wrapper-21">AKIDOMPRO</div>
            </div>
          </div>
        </div>
        <div className="group-16">
          <div className="text-wrapper-18">Administration</div>
          <img className="vector-8" alt="Vector" src="/img/vector-18-1.png" />
        </div>
        <div className="group-17">
          <div className="text-wrapper-18">Paramètre</div>
          <img className="vector-9" alt="Vector" src="/img/vector-18-2.png" />
        </div>
        <div className="group-18">
          <div className="overlap-15">
            <div className="rectangle-6" />
            <div className="group-19">
              <div className="group-20">
                <div className="text-wrapper-22">Géoportail RDUE</div>
                <img className="vector-5" alt="Vector" src="/img/vector-5.png" />
              </div>
            </div>
          </div>
        </div>
        <Link className="group-21" to="/dashboard-6">
          <div className="text-wrapper-19">Géoportail planning</div>
          <img className="vector-10" alt="Vector" src="/img/vector-6.png" />
        </Link>
        <div className="group-22">
          <div className="text-wrapper-19">Enquête sociale</div>
          <img className="vector-10" alt="Vector" src="/img/vector-6.png" />
        </div>
        <Link className="group-23" to="/dashboard-9">
          <div className="text-wrapper-19">Project</div>
          <img className="vector-11" alt="Vector" src="/img/vector-8.png" />
        </Link>
      </div>
    </div>
  );
};
