#!/usr/bin/env python3
"""
Route Debugging Script
Checks all routes for issues, conflicts, and proper setup.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from app import create_app
from collections import defaultdict
import re

def extract_routes(app):
    """Extract all routes from Flask app."""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
            'path': rule.rule,
            'blueprint': rule.endpoint.split('.')[0] if '.' in rule.endpoint else 'main'
        })
    return routes

def check_route_issues(routes):
    """Check for common route issues."""
    issues = []
    warnings = []
    
    # Group routes by path
    path_routes = defaultdict(list)
    endpoint_routes = defaultdict(list)
    
    for route in routes:
        path_routes[route['path']].append(route)
        endpoint_routes[route['endpoint']].append(route)
    
    # Check for duplicate paths with same methods
    for path, route_list in path_routes.items():
        if len(route_list) > 1:
            methods_by_path = defaultdict(list)
            for route in route_list:
                for method in route['methods']:
                    methods_by_path[method].append(route)
            
            for method, routes_with_method in methods_by_path.items():
                if len(routes_with_method) > 1:
                    issues.append({
                        'type': 'DUPLICATE_ROUTE',
                        'severity': 'ERROR',
                        'path': path,
                        'method': method,
                        'routes': [r['endpoint'] for r in routes_with_method]
                    })
    
    # Check for authentication on sensitive routes
    auth_required_paths = [
        '/dashboard', '/clients', '/sessions', '/programs',
        '/settings', '/api/v1'
    ]
    
    for route in routes:
        path = route['path']
        # Check if API routes have proper prefixes
        if path.startswith('/api/v1') and not path.startswith('/api/v1/'):
            warnings.append({
                'type': 'API_ROUTE_FORMAT',
                'severity': 'WARNING',
                'path': path,
                'endpoint': route['endpoint']
            })
        
        # Check for trailing slashes inconsistency
        if path != '/' and path.endswith('/') and path[:-1] in path_routes:
            warnings.append({
                'type': 'TRAILING_SLASH',
                'severity': 'WARNING',
                'path': path,
                'endpoint': route['endpoint']
            })
    
    # Check for redirect loops
    redirect_patterns = [
        (r'/dashboard.*', r'/dashboard'),
        (r'/.*', r'/'),
    ]
    
    return issues, warnings

def check_blueprint_registration():
    """Check if all blueprints are properly registered."""
    app = create_app()
    registered_blueprints = set(app.blueprints.keys())
    
    expected_blueprints = {
        'auth', 'main', 'clients', 'sessions', 'programs',
        'calendar', 'api', 'intake', 'marketing', 'workflow',
        'settings', 'exercise_library', 'api_chatbot',
        'api_clients', 'api_sessions', 'api_exercises',
        'api_programs', 'api_progress', 'api_nutrition',
        'api_booking', 'api_payments', 'api_dashboard',
        'api_organization', 'api_user', 'api_settings',
        'api_zoom', 'api_stripe'
    }
    
    missing = expected_blueprints - registered_blueprints
    extra = registered_blueprints - expected_blueprints
    
    return missing, extra, registered_blueprints

def generate_route_report():
    """Generate comprehensive route report."""
    print("=" * 80)
    print("ROUTE DEBUGGING REPORT")
    print("=" * 80)
    print()
    
    app = create_app()
    routes = extract_routes(app)
    
    # Group by blueprint
    by_blueprint = defaultdict(list)
    for route in routes:
        by_blueprint[route['blueprint']].append(route)
    
    print(f"Total Routes: {len(routes)}")
    print(f"Total Blueprints: {len(by_blueprint)}")
    print()
    
    # Check blueprint registration
    print("=" * 80)
    print("BLUEPRINT REGISTRATION CHECK")
    print("=" * 80)
    missing, extra, registered = check_blueprint_registration()
    
    if missing:
        print(f"⚠️  MISSING BLUEPRINTS ({len(missing)}):")
        for bp in sorted(missing):
            print(f"   - {bp}")
    else:
        print("✅ All expected blueprints are registered")
    
    if extra:
        print(f"\nℹ️  EXTRA BLUEPRINTS ({len(extra)}):")
        for bp in sorted(extra):
            print(f"   - {bp}")
    
    print()
    
    # Route issues
    print("=" * 80)
    print("ROUTE ISSUES CHECK")
    print("=" * 80)
    issues, warnings = check_route_issues(routes)
    
    if issues:
        print(f"❌ ERRORS FOUND ({len(issues)}):")
        for issue in issues:
            print(f"\n   Type: {issue['type']}")
            print(f"   Path: {issue['path']}")
            print(f"   Method: {issue['method']}")
            print(f"   Conflicting Routes: {', '.join(issue['routes'])}")
    else:
        print("✅ No route conflicts found")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings[:10]:  # Show first 10
            print(f"   - {warning['type']}: {warning['path']} ({warning['endpoint']})")
        if len(warnings) > 10:
            print(f"   ... and {len(warnings) - 10} more warnings")
    
    print()
    
    # Route summary by blueprint
    print("=" * 80)
    print("ROUTE SUMMARY BY BLUEPRINT")
    print("=" * 80)
    for blueprint in sorted(by_blueprint.keys()):
        blueprint_routes = by_blueprint[blueprint]
        print(f"\n{blueprint.upper()} ({len(blueprint_routes)} routes):")
        for route in sorted(blueprint_routes, key=lambda x: x['path']):
            methods = ', '.join(sorted(route['methods']))
            print(f"   {methods:20} {route['path']}")
    
    print()
    
    # Critical routes check
    print("=" * 80)
    print("CRITICAL ROUTES CHECK")
    print("=" * 80)
    
    critical_routes = {
        '/': 'Homepage',
        '/login': 'Login',
        '/logout': 'Logout',
        '/register': 'Register',
        '/dashboard': 'Dashboard',
        '/api/v1/user/profile': 'User Profile API',
        '/health': 'Health Check'
    }
    
    route_paths = {r['path']: r for r in routes}
    
    for path, name in critical_routes.items():
        if path in route_paths:
            route = route_paths[path]
            methods = ', '.join(sorted(route['methods']))
            print(f"✅ {name:25} {path:30} [{methods}]")
        else:
            # Check for similar paths
            similar = [r['path'] for r in routes if path.split('/')[1] == r['path'].split('/')[1]]
            if similar:
                print(f"⚠️  {name:25} {path:30} (similar: {similar[0]})")
            else:
                print(f"❌ {name:25} {path:30} NOT FOUND")
    
    print()
    print("=" * 80)
    print("DEBUG COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    try:
        generate_route_report()
    except Exception as e:
        print(f"Error generating report: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

