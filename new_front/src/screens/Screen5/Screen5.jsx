import React from "react";
import { Link } from "react-router-dom";
import { Group } from "../../components/Group";
import "./style.css";

export const Screen5 = () => {
  return (
    <div className="screen-5">
      <div className="dashboard-5">
        <div className="rectangle-31" />
        <div className="overlap-46">
          <div className="group-118">
            <div className="group-119">
              <div className="overlap-group-15">
                <div className="rectangle-32" />
                <div className="text-wrapper-125">Rechercher ici...</div>
                <div className="rectangle-33" />
                <img className="vector-54" alt="Vector" src="/img/vector-21.png" />
              </div>
            </div>
          </div>
          <div className="group-120">
            <div className="overlap-47">
              <div className="text-wrapper-126">Choisir une Coopérative</div>
              <img className="vector-55" alt="Vector" src="/img/vector-25.png" />
            </div>
          </div>
          <div className="group-121">
            <div className="group-122">
              <div className="group-123">
                <img className="group-124" alt="Group" src="/img/group-221-1.png" />
              </div>
              <div className="group-125">
                <div className="overlap-group-16">
                  <div className="text-wrapper-127">Choisir un fichier</div>
                  <div className="text-wrapper-128">KML</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="text-wrapper-129">Details Géoportail planting</div>
        <img className="vector-56" alt="Vector" src="/img/vector-8-4.png" />
        <div className="overlap-48">
          <div className="group-126">
            <div className="group-127">
              <img className="vector-57" alt="Vector" src="/img/vector-31-1.png" />
            </div>
            <div className="group-128">
              <img className="group-129" alt="Group" src="/img/group-236.png" />
            </div>
            <Group className="group-256-instance" group="/img/group-234.png" property1="default" />
          </div>
        </div>
        <div className="overlap-49">
          <div className="rectangle-34" />
          <div className="group-130">
            <div className="text-wrapper-130">Ndrikro</div>
            <div className="text-wrapper-131">Ndrikro</div>
            <div className="text-wrapper-132">Ndrikro</div>
            <div className="text-wrapper-133">Ndrikro</div>
            <div className="element-17">Offoumpo</div>
            <div className="element-18">Offoumpo</div>
            <div className="element-19">Offoumpo</div>
            <div className="element-20">Offoumpo</div>
            <div className="element-21">Boa Vincent</div>
            <div className="element-22">Boa Vincent</div>
            <div className="element-23">Boa Vincent</div>
            <div className="element-24">Boa Vincent</div>
            <div className="element-25">Bognande</div>
            <div className="element-26">Bognande</div>
            <div className="element-27">Bognande</div>
            <div className="element-28">Bognande</div>
            <div className="element-29">Kouamekro</div>
            <div className="element-30">Kouamekro</div>
            <div className="element-31">Kouamekro</div>
            <div className="element-32">Kouamekro</div>
          </div>
        </div>
        <div className="rectangle-35" />
        <div className="group-131" />
        <img className="rectangle-36" alt="Rectangle" src="/img/rectangle-1-2.png" />
        <div className="rectangle-37" />
        <div className="group-132">
          <div className="text-wrapper-134">RDUE</div>
          <img className="vector-58" alt="Vector" src="/img/vector-18.png" />
        </div>
        <Link className="group-133" to="/dashboard-5">
          <div className="text-wrapper-135">Géoportail RDUE</div>
          <img className="vector-59" alt="Vector" src="/img/vector-2.png" />
        </Link>
        <a
          className="group-134"
          href="https://demo.akidompro.com/analyseCOOPAAHS"
          rel="noopener noreferrer"
          target="_blank"
        >
          <div className="text-wrapper-135">Rapport analyse RDUE</div>
          <img className="vector-59" alt="Vector" src="/img/vector-2.png" />
        </a>
        <div className="group-135">
          <div className="text-wrapper-135">Campagnes</div>
          <img className="vector-60" alt="Vector" src="/img/vector-3.png" />
        </div>
        <Link className="group-136" to="/dashboard-4">
          <div className="group-137">
            <img className="group-138" alt="Group" src="/img/group-206.png" />
            <div className="text-wrapper-135">Coopératives</div>
          </div>
        </Link>
        <Link className="group-139" to="/dashboard-3">
          <img className="img-3" alt="Vector" src="/img/vector-4.png" />
          <div className="text-wrapper-136">Tableau de bord</div>
        </Link>
        <div className="group-140">
          <div className="group-141">
            <div className="overlap-group-17">
              <img className="logo-agro-map-5" alt="Logo agro map" />
              <div className="text-wrapper-137">AKIDOMPRO</div>
            </div>
          </div>
        </div>
        <div className="group-142">
          <div className="text-wrapper-134">Administration</div>
          <img className="vector-61" alt="Vector" src="/img/vector-18-1.png" />
        </div>
        <div className="group-143">
          <div className="text-wrapper-134">Paramètre</div>
          <img className="vector-62" alt="Vector" src="/img/vector-18-2.png" />
        </div>
        <div className="group-144">
          <div className="overlap-group-18">
            <div className="group-145">
              <div className="overlap-group-18">
                <div className="rectangle-38" />
                <div className="rectangle-39" />
              </div>
            </div>
            <div className="group-146">
              <div className="text-wrapper-138">Géoportail planting</div>
              <img className="vector-63" alt="Vector" src="/img/vector-53.png" />
            </div>
          </div>
        </div>
        <Link className="group-147" to="/dashboard-9">
          <div className="text-wrapper-135">Project</div>
          <img className="vector-64" alt="Vector" src="/img/vector-8.png" />
        </Link>
        <div className="group-148">
          <img className="img-3" alt="Ri survey fill" src="/img/ri-survey-fill-1.png" />
          <div className="text-wrapper-136">Enquête sociale</div>
        </div>
      </div>
    </div>
  );
};
