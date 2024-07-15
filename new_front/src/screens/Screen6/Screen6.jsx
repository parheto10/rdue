import React from "react";
import { Link } from "react-router-dom";
import { EnCours } from "../../components/EnCours";
import "./style.css";

export const Screen6 = () => {
  return (
    <div className="screen-6">
      <div className="dashboard-6">
        <div className="rectangle-40" />
        <div className="text-wrapper-139">Liste des projets</div>
        <img className="vector-65" alt="Vector" src="/img/vector-8-7.png" />
        <div className="overlap-50">
          <div className="overlap-51">
            <div className="group-149" />
            <img className="vector-66" alt="Vector" src="/img/vector-10-2.png" />
            <div className="navbar-2">
              <div className="text-wrapper-140">Nom du projet</div>
              <div className="text-wrapper-141">Pays</div>
              <div className="text-wrapper-142">Catégories</div>
              <div className="text-wrapper-143">Statut</div>
              <div className="text-wrapper-144">Details</div>
            </div>
          </div>
          <div className="navbar-3">
            <div className="group-149" />
            <img className="vector-67" alt="Vector" src="/img/vector-10-2.png" />
            <img className="vector-66" alt="Vector" src="/img/vector-10-2.png" />
            <div className="text-wrapper-145">Projet zone 1</div>
            <EnCours className="en-cours-instance" />
            <div className="text-wrapper-146">Côte d’Ivoire</div>
            <div className="text-wrapper-147">REFORESTATION</div>
            <div className="text-wrapper-148">Voir détails</div>
          </div>
          <div className="overlap-52">
            <img className="vector-68" alt="Vector" src="/img/vector-10-2.png" />
            <img className="vector-67" alt="Vector" src="/img/vector-10-2.png" />
            <div className="text-wrapper-145">Projet zone 1</div>
            <EnCours className="en-cours-instance" />
            <div className="text-wrapper-146">Côte d’Ivoire</div>
            <div className="text-wrapper-147">REFORESTATION</div>
            <div className="text-wrapper-148">Voir détails</div>
          </div>
          <div className="navbar-4">
            <img className="vector-67" alt="Vector" src="/img/vector-10-2.png" />
            <div className="text-wrapper-145">Projet zone 1</div>
            <EnCours className="en-cours-instance" />
            <div className="text-wrapper-146">Côte d’Ivoire</div>
            <div className="text-wrapper-149">AGROFORESTERIE</div>
            <div className="text-wrapper-148">Voir détails</div>
          </div>
          <div className="overlap-53">
            <img className="vector-68" alt="Vector" src="/img/vector-10-2.png" />
            <div className="text-wrapper-145">Projet zone 3</div>
            <EnCours className="design-component-instance-node" />
            <div className="text-wrapper-146">Côte d’Ivoire</div>
            <div className="text-wrapper-150">AGROFORESTERIE</div>
            <div className="text-wrapper-148">Voir détails</div>
          </div>
          <img className="vector-69" alt="Vector" src="/img/vector-10-2.png" />
          <img className="vector-70" alt="Vector" src="/img/vector-10-2.png" />
          <img className="vector-71" alt="Vector" src="/img/vector-10-2.png" />
          <div className="text-wrapper-151">Projet zone 1</div>
          <div className="text-wrapper-152">Projet zone 1</div>
          <div className="text-wrapper-153">Projet zone 1</div>
          <div className="text-wrapper-154">Projet zone 2</div>
          <div className="text-wrapper-155">Projet zone 4</div>
          <div className="text-wrapper-156">Côte d’Ivoire</div>
          <div className="text-wrapper-157">AGROFORESTERIE</div>
          <EnCours className="en-cours-2" />
          <EnCours className="en-cours-3" />
          <EnCours className="en-cours-4" />
          <EnCours className="en-cours-5" />
          <div className="text-wrapper-158">Côte d’Ivoire</div>
          <div className="text-wrapper-159">AGRICULTURE</div>
          <div className="text-wrapper-160">Côte d’Ivoire</div>
          <div className="text-wrapper-161">Côte d’Ivoire</div>
          <div className="text-wrapper-162">Côte d’Ivoire</div>
          <div className="text-wrapper-163">AGROFORESTERIE</div>
          <div className="text-wrapper-164">REFORESTATION</div>
          <div className="text-wrapper-165">AGROFORESTERIE</div>
          <div className="text-wrapper-166">Fini</div>
          <div className="text-wrapper-167">1</div>
          <div className="text-wrapper-168">-</div>
          <div className="text-wrapper-169">10</div>
          <Link className="text-wrapper-170" to="/dashboard-10">
            Voir détails
          </Link>
          <div className="text-wrapper-171">Voir détails</div>
          <div className="text-wrapper-172">Voir détails</div>
          <div className="text-wrapper-173">Voir détails</div>
          <div className="text-wrapper-174">Voir détails</div>
          <img className="polygon-2" alt="Polygon" src="/img/polygon-1.png" />
        </div>
        <div className="group-150">
          <div className="overlap-group-19">
            <div className="group-151">
              <div className="rectangle-41" />
            </div>
            <div className="text-wrapper-175">Choisir une Campagne</div>
            <img className="vector-72" alt="Vector" src="/img/vector-25.png" />
          </div>
        </div>
        <div className="group-152">
          <div className="overlap-54">
            <div className="group-153">
              <img className="vector-73" alt="Vector" src="/img/vector-33.png" />
            </div>
            <div className="text-wrapper-176">Télécharger la liste</div>
          </div>
        </div>
        <div className="group-154">
          <div className="overlap-55">
            <div className="group-155">
              <img className="group-156" alt="Group" src="/img/group-221.png" />
            </div>
            <div className="text-wrapper-177">Ajouter un projet</div>
          </div>
        </div>
        <div className="group-157" />
        <div className="group-158">
          <div className="rectangle-42" />
        </div>
        <Link className="group-159" to="/dashboard-4">
          <div className="group-160">
            <img className="group-161" alt="Group" src="/img/group-206.png" />
            <div className="text-wrapper-178">Coopératives</div>
          </div>
        </Link>
        <Link className="group-162" to="/dashboard-3">
          <img className="img-4" alt="Vector" src="/img/vector-4.png" />
          <div className="text-wrapper-179">Tableau de bord</div>
        </Link>
        <div className="group-163">
          <div className="group-164">
            <div className="overlap-group-20">
              <img className="logo-agro-map-6" alt="Logo agro map" />
              <div className="text-wrapper-180">AKIDOMPRO</div>
            </div>
          </div>
        </div>
        <div className="group-165">
          <div className="text-wrapper-181">Administration</div>
          <img className="vector-74" alt="Vector" src="/img/vector-18-1.png" />
        </div>
        <div className="group-166">
          <div className="text-wrapper-181">RDUE</div>
          <img className="vector-75" alt="Vector" src="/img/vector-18-15.png" />
        </div>
        <div className="group-167">
          <div className="text-wrapper-181">Paramètre</div>
          <img className="vector-76" alt="Vector" src="/img/vector-18-16.png" />
        </div>
        <Link className="group-168" to="/dashboard-6">
          <div className="text-wrapper-182">Géoportail planning</div>
          <img className="vector-77" alt="Vector" src="/img/vector-36.png" />
        </Link>
        <Link className="group-169" to="/dashboard-5">
          <div className="text-wrapper-182">Géoportail RDUE</div>
          <img className="vector-78" alt="Vector" src="/img/vector-37.png" />
        </Link>
        <a
          className="group-170"
          href="https://demo.akidompro.com/analyseCOOPAAHS"
          rel="noopener noreferrer"
          target="_blank"
        >
          <div className="text-wrapper-182">Rapport analyse RDUE</div>
          <img className="vector-78" alt="Vector" src="/img/vector-37.png" />
        </a>
        <div className="group-171">
          <img className="img-4" alt="Ri survey fill" src="/img/ri-survey-fill-1.png" />
          <div className="text-wrapper-179">Enquête sociale</div>
        </div>
        <div className="group-172">
          <div className="overlap-56">
            <div className="group-173">
              <div className="group-174" />
              <div className="rectangle-43" />
            </div>
            <div className="group-175">
              <div className="text-wrapper-183">Project</div>
              <img className="vector-79" alt="Vector" src="/img/vector-75.png" />
            </div>
          </div>
        </div>
        <div className="group-176">
          <div className="text-wrapper-184">Campagnes</div>
          <img className="vector-80" alt="Vector" src="/img/vector-34.png" />
        </div>
      </div>
    </div>
  );
};
