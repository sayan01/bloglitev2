#!/bin/bash
VIRT_ENV="bin"
check_requirements(){
  rc=0
  echo "Checking neccesary constraints to run the project"
  echo -ne "1. requirements.txt exists\t"
  if [[ -r "requirements.txt" ]] 
  then
    echo "OK" 
  else
    echo "NO" 
    rc=1
  fi

  echo -ne "2. virtual env exists\t"
  if [[ -r "$VIRT_ENV/bin/activate" ]] 
  then
    echo "OK" 
  else
    echo "NO, setting up" 
    if ! python -m venv "$VIRT_ENV" 
    then
      echo "Unable to set up virtual env"
      rc=1
    fi
  fi

  echo -ne "3. .env exists\t"
  if [[ -r ".env" ]] 
  then
    echo "OK" 
  else
    if [[ -r ".env.demo" ]]
    then
      echo "NO, copying .env.demo to .env" 
      cp .env.demo .env 
      echo "SECRET_KEY=$(date +%s%N | sha512sum | cut -d' ' -f1)" >> .env
    else
      echo "NO, and neither does .env.demo"
      rc=1
    fi
  fi

  return "$rc"
}
if check_requirements 
then
  echo "All requirements satisfied" 
else
  echo "Requirements not satisfied" 
  exit 1 
fi
echo "Using virtual env located at $VIRT_ENV"
if ! source "$VIRT_ENV/bin/activate" 
then
  echo "Error Occurred" 
  exit 1 
fi
echo "Installing all requirements"
if ! pip install -qqr requirements.txt  
then
  echo "Error Occurred" 
  exit 1 
fi
echo "Running flask server"
if ! flask run 
then
  echo "Error Occurred" 
  exit 1
fi
