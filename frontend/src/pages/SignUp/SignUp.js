import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { Button, TextField } from '@mui/material';

const SignUp = () => {
  const initialValues = { email: '', password: '', confirmPassword: '' };

  const validationSchema = Yup.object({
    email: Yup.string().email('Invalid email').required('Required'),
    password: Yup.string().required('Required'),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref('password'), null], 'Passwords must match')
      .required('Required'),
  });

  const onSubmit = (values) => {
    console.log(values);
  };

  return (
    <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
      <Form>
        <Field as={TextField} name="email" label="Email" fullWidth />
        <ErrorMessage name="email" component="div" />
        <Field as={TextField} name="password" label="Password" type="password" fullWidth />
        <ErrorMessage name="password" component="div" />
        <Field as={TextField} name="confirmPassword" label="Confirm Password" type="password" fullWidth />
        <ErrorMessage name="confirmPassword" component="div" />
        <Button type="submit" variant="contained" color="primary">
          Sign Up
        </Button>
      </Form>
    </Formik>
  );
};

export default SignUp;