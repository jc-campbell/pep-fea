#!/usr/bin/env python3
import glob
import os
import re
import vtk


def convert_file(legacy_file):
    print(f"Converting {legacy_file} ...")
    # Use the generic reader to read legacy VTK files
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(legacy_file)
    reader.Update()

    data = reader.GetOutput()
    if data is None:
        print(f"Warning: Could not read {legacy_file}")
        return None, None

    # Determine the dataset type and choose the correct writer/extension
    writer = None
    extension = None
    dataType = data.GetClassName()

    if data.IsA("vtkPolyData"):
        writer = vtk.vtkXMLPolyDataWriter()
        extension = ".vtp"
    elif data.IsA("vtkUnstructuredGrid"):
        writer = vtk.vtkXMLUnstructuredGridWriter()
        extension = ".vtu"
    elif data.IsA("vtkStructuredGrid"):
        writer = vtk.vtkXMLStructuredGridWriter()
        extension = ".vts"
    elif data.IsA("vtkRectilinearGrid"):
        writer = vtk.vtkXMLRectilinearGridWriter()
        extension = ".vtr"
    else:
        print(f"Dataset type not supported for {legacy_file}: {dataType}")
        return None, None

    # Build the output filename: replace the .vtk extension with the new one
    xml_file = os.path.splitext(legacy_file)[0] + extension
    writer.SetFileName(xml_file)
    writer.SetInputData(data)
    # Uncomment next line to write binary (default is ASCII)
    # writer.SetDataModeToBinary()
    writer.Write()

    print(f"Converted {legacy_file} ({dataType}) to {xml_file}")
    return xml_file, dataType


def convert_all_legacy_files():
    # Recursively find all legacy .vtk files
    legacy_files = glob.glob("**/*.vtk", recursive=True)
    converted_files = []  # List of tuples: (directory, filename)
    for legacy_file in legacy_files:
        xml_file, dtype = convert_file(legacy_file)
        if xml_file:
            # Save the relative path and filename
            dirpath = os.path.dirname(xml_file)
            converted_files.append((dirpath, os.path.basename(xml_file)))
    return converted_files


def generate_pvd_in_directory(dirpath, files):
    # Group files by common series prefix.
    # Expect filenames of the form: PREFIX_TIME.ext
    series = {}
    pattern = re.compile(r'^(.*_)([0-9]+(?:\.[0-9]+)?)\.(vtu|vtp|vts|vtr)$')
    for fname in files:
        m = pattern.match(fname)
        if m:
            prefix = m.group(1)  # includes trailing underscore
            time_str = m.group(2)
            ext = m.group(3)
            try:
                timestep = float(time_str)
            except ValueError:
                continue
            series.setdefault(prefix, []).append((fname, timestep))
    # For each series, sort by timestep and write a .pvd file
    for prefix, items in series.items():
        items.sort(key=lambda x: x[1])
        # Remove the trailing underscore for the pvd filename
        series_name = prefix.rstrip('_')
        pvd_filename = os.path.join(dirpath, series_name + ".pvd")
        with open(pvd_filename, "w") as pvd:
            pvd.write('<?xml version="1.0"?>\n')
            pvd.write(
                '<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n')
            pvd.write('  <Collection>\n')
            for fname, timestep in items:
                pvd.write(
                    f'    <DataSet timestep="{timestep}" group="" part="0" file="{fname}"/>\n')
            pvd.write('  </Collection>\n')
            pvd.write('</VTKFile>\n')
        print(f"Generated {pvd_filename} with {len(items)} entries.")


def generate_pvd_files(converted_files):
    # Organize by directory
    dirs = {}
    for dirpath, fname in converted_files:
        dirs.setdefault(dirpath, []).append(fname)
    # For each directory, if there are any converted files, generate pvd files
    for dirpath, files in dirs.items():
        generate_pvd_in_directory(dirpath, files)


def main():
    print("Starting conversion of legacy VTK files...")
    converted_files = convert_all_legacy_files()
    print("Conversion complete.")
    print("Generating .pvd files...")
    generate_pvd_files(converted_files)
    print("Done.")


if __name__ == "__main__":
    main()
