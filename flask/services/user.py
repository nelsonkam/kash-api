from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from utils.graphql import graphql