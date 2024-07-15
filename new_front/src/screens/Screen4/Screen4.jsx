import React from "react";
import { Link } from "react-router-dom";
import { Group } from "../../components/Group";
import "./style.css";

export const Screen4 = () => {
  return (
    <div className="screen-4">
      <div className="dashboard-4">
        <div className="rectangle-20" />
        <div className="text-wrapper-107">Details coopérative</div>
        <img className="vector-42" alt="Vector" src="/img/vector-8-2.png" />
        <div className="overlap-40">
          <div className="group-87">
            <div className="group-88">
              <img className="vector-43" alt="Vector" src="/img/vector-31-1.png" />
            </div>
            <div className="group-89">
              <img className="group-90" alt="Group" src="/img/group-236.png" />
            </div>
            <Group className="group-256" group="/img/group-234-1.png" property1="default" />
          </div>
        </div>
        <div className="overlap-41">
          <div className="rectangle-21" />
          <div className="group-91">
            <div className="text-wrapper-108">Ndrikro</div>
            <div className="text-wrapper-109">Ndrikro</div>
            <div className="text-wrapper-110">Ndrikro</div>
            <div className="text-wrapper-111">Ndrikro</div>
            <div className="element">Offoumpo</div>
            <div className="element-2">Offoumpo</div>
            <div className="element-3">Offoumpo</div>
            <div className="element-4">Offoumpo</div>
            <div className="element-5">Boa Vincent</div>
            <div className="element-6">Boa Vincent</div>
            <div className="element-7">Boa Vincent</div>
            <div className="element-8">Boa Vincent</div>
            <div className="element-9">Bognande</div>
            <div className="element-10">Bognande</div>
            <div className="element-11">Bognande</div>
            <div className="element-12">Bognande</div>
            <div className="element-13">Kouamekro</div>
            <div className="element-14">Kouamekro</div>
            <div className="element-15">Kouamekro</div>
            <div className="element-16">Kouamekro</div>
          </div>
        </div>
        <div className="overlap-42">
          <div className="group-92">
            <div className="group-93">
              <div className="overlap-group-12">
                <div className="rectangle-22" />
                <div className="text-wrapper-112">Rechercher ici...</div>
                <div className="rectangle-23" />
                <img className="vector-44" alt="Vector" src="/img/vector-21.png" />
              </div>
            </div>
          </div>
          <div className="group-94">
            <div className="overlap-43">
              <div className="text-wrapper-113">Choisir une Coopérative</div>
              <img className="vector-45" alt="Vector" src="/img/vector-25.png" />
            </div>
          </div>
          <div className="group-95">
            <div className="group-96">
              <div className="group-97">
                <img className="group-98" alt="Group" src="/img/group-221-1.png" />
              </div>
              <div className="group-99">
                <div className="overlap-group-13">
                  <div className="text-wrapper-114">Choisir un fichier</div>
                  <div className="text-wrapper-115">KML</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="overlap-44">
          <div className="rectangle-24" />
          <div className="rectangle-25" />
          <div className="rectangle-26" />
          <div className="rectangle-27" />
          <p className="text-wrapper-116">Zone à plus de 2 km d’espace protégé</p>
          <p className="text-wrapper-117">Zone à moins de 2km d’espace protégé</p>
          <div className="text-wrapper-118">ADEBEM(LAKOTA)</div>
          <div className="text-wrapper-119">Zone de concentration</div>
        </div>
        <div className="group-100" />
        <img className="rectangle-28" alt="Rectangle" src="/img/rectangle-1.png" />
        <div className="rectangle-29" />
        <div className="group-101">
          <div className="text-wrapper-120">RDUE</div>
          <img className="vector-46" alt="Vector" src="/img/vector-18.png" />
        </div>
        <a
          className="group-102"
          href="https://demo.akidompro.com/analyseCOOPAAHS"
          rel="noopener noreferrer"
          target="_blank"
        >
          <div className="text-wrapper-121">Rapport analyse RDUE</div>
          <img className="vector-47" alt="Vector" src="/img/vector-2.png" />
        </a>
        <div className="group-103">
          <div className="text-wrapper-121">Campagnes</div>
          <img className="vector-48" alt="Vector" src="/img/vector-3.png" />
        </div>
        <Link className="group-104" to="/dashboard-4">
          <div className="group-105">
            <img className="group-106" alt="Group" src="/img/group-206.png" />
            <div className="text-wrapper-121">Coopératives</div>
          </div>
        </Link>
        <Link className="group-107" to="/dashboard-3">
          <img className="vector-49" alt="Vector" src="/img/vector-4.png" />
          <div className="text-wrapper-122">Tableau de bord</div>
        </Link>
        <div className="group-108">
          <div className="group-109">
            <div className="overlap-group-14">
              <img className="logo-agro-map-4" alt="Logo agro map" />
              <div className="text-wrapper-123">AKIDOMPRO</div>
            </div>
          </div>
        </div>
        <div className="group-110">
          <div className="text-wrapper-120">Administration</div>
          <img className="vector-50" alt="Vector" src="/img/vector-18-1.png" />
        </div>
        <div className="group-111">
          <div className="text-wrapper-120">Paramètre</div>
          <img className="vector-51" alt="Vector" src="/img/vector-18-2.png" />
        </div>
        <div className="group-112">
          <div className="overlap-45">
            <div className="rectangle-30" />
            <div className="group-113">
              <div className="group-114">
                <div className="text-wrapper-124">Géoportail RDUE</div>
                <img className="vector-47" alt="Vector" src="/img/vector-5.png" />
              </div>
            </div>
          </div>
        </div>
        <Link className="group-115" to="/dashboard-6">
          <div className="text-wrapper-121">Géoportail planning</div>
          <img className="vector-52" alt="Vector" src="/img/vector-45.png" />
        </Link>
        <div className="group-116">
          <div className="text-wrapper-121">Enquête sociale</div>
          <img className="vector-52" alt="Vector" src="/img/vector-45.png" />
        </div>
        <Link className="group-117" to="/dashboard-9">
          <div className="text-wrapper-121">Project</div>
          <img className="vector-53" alt="Vector" src="/img/vector-8.png" />
        </Link>
      </div>
    </div>
  );
};
