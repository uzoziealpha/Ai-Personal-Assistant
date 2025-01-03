import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { Button, TextField } from '@mui/material';

const SignIn = () => {
  const initialValues = { email: '', password: '' };

  const validationSchema = Yup.object({
    email: Yup.string().email('Invalid email').required('Required'),
    password: Yup.string().required('Required'),
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
        <Button type="submit" variant="contained" color="primary">
          Sign In
        </Button>
      </Form>
    </Formik>
  );
};

export default SignIn;